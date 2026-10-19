"""Functional fixtures for project setup, command execution and agent adapters."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import overlay

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("kun", HERE / "kun.py")
kun = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kun)
kun.INSTALL = Path.home() / ".local/share/kun"
kun.VENDOR = kun.INSTALL / "firstmate"


def command(args, cwd=None, env=None, check=True):
    result = subprocess.run([str(x) for x in args], cwd=cwd, env=env, text=True, capture_output=True, timeout=60)
    if check and result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return result


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kun-test-", dir="/private/tmp")
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "project with spaces"
        self.root.mkdir()
        self.data = self.base / "private"
        kun.DATA = self.data
        command(["git", "init", "-q", "-b", "main"], self.root)
        self.instructions = "# Existing project instructions\nDo not replace me.\n"
        (self.root / "AGENTS.md").write_text(self.instructions)
        (self.root / "package.json").write_text(json.dumps({"name": "kun-fixture", "private": True, "scripts": {
            "test": 'node -e "console.log(\'fixture passed\')"', "build": "node -e \"process.exit(0)\""}}))
        command(["git", "add", "AGENTS.md", "package.json"], self.root)
        command(["git", "-c", "user.name=Kun Check", "-c", "user.email=kun-check@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"], self.root)

    def tearDown(self):
        self.temp.cleanup()

    def env(self):
        return {**os.environ, "KUN_INSTALL_ROOT": str(kun.INSTALL), "KUN_HOME": str(self.data)}

    def cli(self, *args, check=True):
        return command([sys.executable, HERE / "kun.py", *args], self.root, self.env(), check=check)

    def test_nested_folder_resolves_actual_git_root(self):
        nested = self.root / "src/nested"
        nested.mkdir(parents=True)
        self.assertEqual(kun.project_root(nested), self.root)

    def test_setup_preserves_dirty_work_and_project_instructions(self):
        (self.root / "personal.txt").write_text("uncommitted content")
        before = command(["git", "status", "--porcelain"], self.root).stdout
        config = kun.setup(self.root, mode="local-only")
        self.assertEqual(command(["git", "status", "--porcelain"], self.root).stdout, before)
        self.assertEqual((self.root / "AGENTS.md").read_text(), self.instructions)
        self.assertEqual((self.root / "personal.txt").read_text(), "uncommitted content")
        self.assertTrue(config["detected"]["dirty"])
        self.assertEqual((Path(config["home"]) / "projects" / config["name"]).resolve(), self.root)

    def test_repeat_setup_keeps_preferences_and_other_registry_entries(self):
        config = kun.setup(self.root, mode="local-only")
        home = Path(config["home"])
        (home / "data/captain.md").write_text("My own preferences\n")
        with (home / "data/projects.md").open("a") as stream:
            stream.write("- extra [local-only] - Another registered project\n")
        again = kun.setup(self.root)
        self.assertEqual(config["home"], again["home"])
        self.assertEqual((home / "data/captain.md").read_text(), "My own preferences\n")
        self.assertIn("- extra [local-only]", (home / "data/projects.md").read_text())

    def test_native_registry_mode_is_preserved_and_reported(self):
        command(["git", "remote", "add", "origin", "https://github.com/example/fixture.git"], self.root)
        config = kun.setup(self.root, mode="local-only")
        registry = Path(config["home"]) / "data/projects.md"
        registry.write_text(registry.read_text().replace("[local-only ", "[no-mistakes "))
        # Avoid initializing a real daemon in this functional fixture.
        gate = Path(kun.environment(Path(config["home"]))["NM_HOME"]) / "gate.git"
        command(["git", "remote", "add", "no-mistakes", str(gate)], self.root)
        self.assertEqual(kun.setup(self.root)["mode"], "no-mistakes")

    def test_reopening_preserves_custom_worker_rules_and_default_array(self):
        config = kun.setup(self.root, mode="local-only")
        dispatch = Path(config["home"]) / "config/crew-dispatch.json"
        preferences = {
            "rules": [{"when": "A small refactor", "use": {"harness": "codex"}}],
            "default": [{"harness": "codex", "model": "fixture-model", "effort": "high"}],
        }
        original = json.dumps(preferences, indent=4) + "\n"
        dispatch.write_text(original)
        self.cli("setup")
        self.cli("start", "--print")
        self.assertEqual(dispatch.read_text(), original)
        self.assertEqual(json.loads((Path(config["home"]) / "project.json").read_text())["agent"], "codex")

    def test_explicit_assistant_change_preserves_rules_and_replaces_only_default(self):
        config = kun.setup(self.root, mode="local-only")
        dispatch = Path(config["home"]) / "config/crew-dispatch.json"
        rules = [{"when": "A small refactor", "use": {"harness": "codex"}}]
        dispatch.write_text(json.dumps({"rules": rules, "default": [{"harness": "codex", "model": "fixture-model"}]}))
        self.cli("setup", "--agent", "claude")
        self.assertEqual(json.loads(dispatch.read_text()), {"rules": rules, "default": {"harness": "claude"}})

    def test_invalid_routing_is_reported_without_overwriting_project_preferences(self):
        config = kun.setup(self.root, mode="local-only")
        home = Path(config["home"])
        dispatch = home / "config/crew-dispatch.json"
        previous = (home / "project.json").read_bytes()
        for content in ('{"rules": [', '[]', 'null'):
            with self.subTest(content=content):
                dispatch.write_text(content)
                result = self.cli("setup", "--agent", "claude", check=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("crew-dispatch.json", result.stderr)
                self.assertEqual(dispatch.read_text(), content)
                self.assertEqual((home / "project.json").read_bytes(), previous)

    def test_firstmate_registry_accepts_generated_posture(self):
        config = kun.setup(self.root, mode="local-only")
        env = kun.environment(Path(config["home"]))
        result = command(["bash", kun.VENDOR / "bin/fm-project-mode.sh", config["name"]], env=env)
        self.assertEqual(result.stdout.strip(), "local-only off")
        result = command(["bash", kun.VENDOR / "bin/fm-project-mode.sh", "--branch-prefix", config["name"]], env=env)
        self.assertEqual(result.stdout.strip(), "codex/")

    def test_distinct_projects_have_distinct_state(self):
        first = kun.setup(self.root, mode="local-only")
        second_root = self.base / "other/project with spaces"
        second_root.parent.mkdir()
        command(["git", "clone", "-q", str(self.root), str(second_root)])
        second = kun.setup(second_root, mode="local-only")
        self.assertNotEqual(first["id"], second["id"])
        self.assertNotEqual(first["home"], second["home"])

    def test_remote_credentials_are_not_recorded(self):
        command(["git", "remote", "add", "origin", "https://user:secret-token@github.com/example/fixture.git?token=secret"], self.root)
        config = kun.setup(self.root, mode="local-only")
        self.assertEqual(config["detected"]["origin"], "https://github.com/example/fixture.git")
        self.assertNotIn("secret", (Path(config["home"]) / "project.json").read_text())

    def test_language_checks_are_detected_without_running_them(self):
        info = kun.detect(self.root)
        self.assertEqual(next(c["argv"] for c in info["checks"] if c["kind"] == "test"), ["npm", "run", "test"])
        (self.root / "pyproject.toml").write_text('[project]\nname="fixture"\nversion="0"\ndependencies=["pytest"]\n[tool.ruff]\n')
        (self.root / "uv.lock").write_text("")
        checks = kun.detect(self.root)["checks"]
        self.assertTrue(any(c["argv"] == ["uv", "run", "python", "-m", "pytest"] for c in checks))
        self.assertTrue(all(c["verified"] is False for c in checks))

    def test_placeholder_node_test_is_not_a_real_check(self):
        (self.root / "package.json").write_text(json.dumps({"scripts": {"test": 'echo "Error: no test specified" && exit 1'}}))
        self.assertFalse(kun.detect(self.root)["checks"])

    def test_check_preview_then_explicit_real_execution(self):
        self.cli("setup", "--mode", "local-only")
        preview = self.cli("check")
        self.assertIn("Preview only", preview.stdout)
        ran = self.cli("check", "--run")
        self.assertIn("fixture passed", ran.stdout)
        _, _, home = kun.identity(self.root)
        self.assertEqual(json.loads((home / "state/last-check.json").read_text())["exit_code"], 0)

    def test_print_launch_does_not_start_an_agent(self):
        output = self.cli("start", "--mode", "local-only", "--print")
        data = json.loads(output.stdout)
        self.assertEqual(data["cwd"], str(kun.VENDOR))
        self.assertTrue(data["argv"][0].endswith("/guards/codex"))
        self.assertIn("onboarding and an explanation only", data["argv"][-1])

    def test_agent_change_updates_pipeline_choice(self):
        config = kun.setup(self.root, mode="local-only")
        changed = kun.setup(self.root, agent="claude")
        self.assertEqual(changed["agent"], "claude")
        env = kun.environment(Path(config["home"]))
        self.assertTrue((Path(env["NM_HOME"]) / "config.yaml").read_text().startswith("agent: claude\n"))

    def test_unborn_and_non_repository_folders_have_actionable_error(self):
        empty = self.base / "empty"
        empty.mkdir()
        with self.assertRaisesRegex(kun.KunError, "Git repository"):
            kun.project_root(empty)
        command(["git", "init", "-q", str(empty)])
        with self.assertRaisesRegex(kun.KunError, "first commit"):
            kun.project_root(empty)

    def test_tmux_starts_real_adapter_and_reuses_live_session(self):
        config = kun.setup(self.root, agent="claude", mode="local-only")
        original = kun.INSTALL
        fake = self.base / "fake install"
        fake.mkdir()
        (fake / "firstmate").symlink_to(kun.VENDOR)
        (fake / "toolchain").symlink_to(original / "toolchain")
        (fake / "guards").mkdir()
        for name in kun.AGENTS:
            (fake / "guards" / name).symlink_to(HERE / "agent_guard.py")
        capture = self.base / "launches.jsonl"
        stub = self.base / "fake-agent"
        stub.write_text(f"#!{sys.executable}\nimport json,os,sys,time\nfrom pathlib import Path\np=Path(os.environ['KUN_CAPTURE'])\nwith p.open('a') as f: f.write(json.dumps({{'argv':sys.argv[1:],'cwd':os.getcwd(),'home':os.environ.get('FM_HOME')}})+'\\n')\nprint('fixture harness ready',flush=True)\ntime.sleep(20)\n")
        stub.chmod(0o755)
        (fake / "installation.json").write_text(json.dumps({"agents": {"claude": str(stub)}}))
        socket = "kun-check-" + config["id"]
        try:
            kun.INSTALL = fake
            with patch.dict(os.environ, {"KUN_TMUX_SOCKET": socket, "KUN_CAPTURE": str(capture)}):
                kun.launch(config, attach=False)
                deadline = time.monotonic() + 10
                while not capture.exists() and time.monotonic() < deadline:
                    time.sleep(0.05)
                self.assertTrue(capture.exists(), "The real tmux pane did not execute the adapter")
                record = json.loads(capture.read_text().splitlines()[0])
                self.assertEqual(record["home"], config["home"])
                self.assertEqual(Path(record["cwd"]).resolve(), kun.VENDOR.resolve())
                kun.launch(config, attach=False)
                self.assertEqual(len(capture.read_text().splitlines()), 1, "Reopening duplicated the running agent")
        finally:
            kun.INSTALL = original
            command(["tmux", "-L", socket, "kill-server"], check=False)


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kun-guard-", dir="/private/tmp")
        self.base = Path(self.temp.name)
        stub = self.base / "capture"
        stub.write_text(f"#!{sys.executable}\nimport json,os,sys\nfrom pathlib import Path\nPath(os.environ['KUN_CAPTURE']).write_text(json.dumps({{'argv':sys.argv[1:],'opencode':os.environ.get('OPENCODE_CONFIG_CONTENT'),'legacy_permission':os.environ.get('OPENCODE_PERMISSION')}}))\n")
        stub.chmod(0o755)
        (self.base / "installation.json").write_text(json.dumps({"agents": {name: str(stub) for name in kun.AGENTS}}))
        for name in kun.AGENTS:
            (self.base / name).symlink_to(HERE / "agent_guard.py")

    def tearDown(self):
        self.temp.cleanup()

    def capture(self, name, args, extra=None):
        output = self.base / "captured.json"
        env = {**os.environ, "KUN_INSTALL_ROOT": str(self.base), "KUN_CAPTURE": str(output), "FM_HOME": "/private/tmp/project home"}
        env.update(extra or {})
        command([self.base / name, *args], env=env)
        return json.loads(output.read_text())

    def test_claude_bypass_is_replaced_by_classifier_review(self):
        result = self.capture("claude", ["--dangerously-skip-permissions", "task"])
        self.assertEqual(result["argv"], ["--permission-mode", "auto", "task"])

    def test_codex_keeps_sandbox_and_approval_controls(self):
        result = self.capture("codex", ["exec", "--dangerously-bypass-approvals-and-sandbox", "-c", 'sandbox_mode="danger-full-access"', "--config=approval_policy=never", "-sdanger-full-access", "task"])
        self.assertEqual(result["argv"][:4], ["--sandbox", "workspace-write", "-c", 'approval_policy="on-request"'])
        self.assertIn("/private/tmp/project home", result["argv"])
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", result["argv"])
        self.assertNotIn("--config=approval_policy=never", result["argv"])

    def test_opencode_does_not_inherit_blanket_allow(self):
        result = self.capture("opencode", ["--prompt", "task"], {"OPENCODE_CONFIG_CONTENT": '{"permission":{"*":"allow"},"model":"example"}', "OPENCODE_PERMISSION": '{"*":"allow"}'})
        content = json.loads(result["opencode"])
        self.assertEqual(content["permission"], {"*": "ask"})
        self.assertEqual(content["model"], "example")
        self.assertIsNone(result["legacy_permission"])

    def test_version_probe_does_not_acquire_run_flags(self):
        self.assertEqual(self.capture("codex", ["--version"])["argv"], ["--version"])

    def test_native_worker_template_uses_guard_after_path_reordering(self):
        # Include spaces and an apostrophe to exercise nested shell quoting.
        prefix = self.base / "install with 'quotes"
        prefix.mkdir()
        (prefix / "guards").mkdir()
        (prefix / "guards/codex").symlink_to(HERE / "agent_guard.py")
        shutil.copy2(self.base / "installation.json", prefix / "installation.json")
        original = command(["git", "-C", kun.VENDOR, "show", "HEAD:bin/fm-spawn.sh"]).stdout
        patched = overlay.render("bin/fm-spawn.sh", original, prefix)
        function = patched.split("launch_template() {", 1)[1].split('\n}\n\ncase "$ARG3"', 1)[0]
        rendered = command(["bash", "-c", "launch_template() {" + function + "\n}\nlaunch_template codex ship"]).stdout
        rendered = rendered.replace("__MODELFLAG__", "").replace("__EFFORTFLAG__", "")
        rendered = rendered.replace('"$(__OPINPUT__ encode launch-brief < __BRIEF__)"', "'fixture task'").replace("__TURNEND__", "/private/tmp/kun-turn-end")
        output = self.base / "worker.json"
        env = {**os.environ, "PATH": "/opt/homebrew/bin:/usr/bin:/bin", "KUN_INSTALL_ROOT": str(prefix), "KUN_CAPTURE": str(output)}
        command(["bash", "-c", rendered], env=env)
        argv = json.loads(output.read_text())["argv"]
        self.assertEqual(argv[:4], ["--sandbox", "workspace-write", "-c", 'approval_policy="on-request"'])
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", argv)
        self.assertIn("fixture task", argv)

    def test_linked_project_bootstrap_skips_source_sync(self):
        original = (kun.VENDOR / "bin/fm-bootstrap.sh").read_text()
        # Use pinned source, even after a previous installer applied the overlay.
        original = command(["git", "-C", kun.VENDOR, "show", "HEAD:bin/fm-bootstrap.sh"]).stdout
        patched = overlay.render("bin/fm-bootstrap.sh", original, self.base)
        function = patched.split("fleet_sync() {", 1)[1].split("\n}\n", 1)[0]
        # Failure after the inserted guard would expose a missing early return.
        function = function.replace('[ -x "$FM_ROOT/bin/fm-fleet-sync.sh" ] || return 0', 'echo UNEXPECTED_SYNC; return 1')
        result = command(["bash", "-c", "fleet_sync() {" + function + "\n}\nKUN_LINKED_PROJECTS=1 fleet_sync"])
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)

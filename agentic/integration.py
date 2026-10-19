#!/usr/bin/env python3
"""Exercise installed Firstmate tools against disposable local Git repositories."""
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("kun", HERE / "kun.py")
kun = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kun)
kun.INSTALL = Path.home() / ".local/share/kun"
kun.VENDOR = kun.INSTALL / "firstmate"
results = []


def call(args, cwd=None, env=None, check=True):
    result = subprocess.run([str(x) for x in args], cwd=cwd, env=env, capture_output=True, text=True, timeout=120)
    if check and result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result


def passed(name):
    results.append({"check": name, "passed": True})
    print("PASS:", name, flush=True)


with tempfile.TemporaryDirectory(prefix="kun-live-", dir="/private/tmp") as temp:
    base = Path(temp).resolve()
    kun.DATA = base / "data"
    root = base / "project"
    root.mkdir()
    call(["git", "init", "-q", "-b", "main"], root)
    (root / "README.md").write_text("# Fixture\n")
    call(["git", "add", "README.md"], root)
    call(["git", "-c", "user.name=Kun Integration", "-c", "user.email=kun-check@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture"], root)
    config = kun.setup(root, mode="local-only")
    home = Path(config["home"])
    env = kun.environment(home)
    detect_env = {**env, "FM_BOOTSTRAP_DETECT_ONLY": "1", "FM_BOOTSTRAP_NETWORK": "skip"}
    bootstrap = call(["bash", kun.VENDOR / "bin/fm-bootstrap.sh", "detect"], env=detect_env)
    (HERE.parent / "verification/kun-bootstrap.log").write_text(bootstrap.stdout + bootstrap.stderr)
    assert "MISSING:" not in bootstrap.stdout + bootstrap.stderr, "Firstmate reports an unmet dependency"
    passed("Official Firstmate bootstrap accepts installed tool versions and project home")

    pool = base / "pool"
    lease = call(["treehouse", "get", "--root", pool, "--lease", "--no-fetch", "-b", "codex/integration"], cwd=root, env=env)
    worktree = Path(lease.stdout.strip())
    assert worktree.is_dir()
    assert call(["git", "branch", "--show-current"], worktree).stdout.strip() == "codex/integration"
    assert (worktree / "README.md").read_text() == "# Fixture\n"
    call(["treehouse", "return", "--root", pool, worktree], cwd=root, env=env)
    passed("Treehouse creates a real isolated branch/worktree and releases its lease")

    origin = base / "origin.git"
    call(["git", "init", "--bare", "-q", "-b", "main", origin])
    call(["git", "remote", "add", "origin", origin], root)
    call(["git", "push", "-q", "-u", "origin", "main"], root)
    agents = Path.home() / "Library/LaunchAgents"
    before = set(agents.glob("*no-mistakes*.plist")) if agents.exists() else set()
    try:
        config = kun.setup(root, mode="no-mistakes")
        env = kun.environment(home)
        gate = call(["git", "remote", "get-url", "no-mistakes"], root).stdout.strip()
        assert Path(gate).resolve().is_relative_to(Path(env["NM_HOME"]).resolve())
        assert call(["git", "status", "--porcelain"], root).stdout.strip() == ""
        status = call(["no-mistakes", "daemon", "status"], env=env)
        (HERE.parent / "verification/kun-gate.log").write_text(status.stdout + status.stderr)
        again = kun.setup(root)
        assert again["mode"] == "no-mistakes"
        passed("No Mistakes initializes a real local gate/daemon and repeat setup preserves it")
    finally:
        call(["no-mistakes", "daemon", "stop"], env=env, check=False)
        after = set(agents.glob("*no-mistakes*.plist")) if agents.exists() else set()
        for path in after - before:
            data = plistlib.loads(path.read_bytes())
            if env["NM_HOME"] in json.dumps(data):
                call(["launchctl", "bootout", f"gui/{os.getuid()}/{data['Label']}"], check=False)
                path.unlink()

    record = json.loads((kun.INSTALL / "installation.json").read_text())
    codex = record["agents"]["codex"]
    call([codex, "--sandbox", "workspace-write", "-c", 'approval_policy="on-request"', "--add-dir", home, "exec", "--help"])
    passed("Native Codex accepts the guarded sandbox/approval launch flags without a model request")

(HERE.parent / "verification/kun-integration-results.json").write_text(json.dumps(results, indent=2) + "\n")
print("Installed-tool integration checks passed; no model requests made.")

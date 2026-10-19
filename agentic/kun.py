#!/usr/bin/env python3
"""Initialize or reopen a project-scoped Firstmate environment with `kun`."""
import argparse
from datetime import date
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tomllib
import time
from urllib.parse import urlsplit, urlunsplit

INSTALL = Path(os.environ.get("KUN_INSTALL_ROOT", Path(__file__).resolve().parents[1]))
DATA = Path(os.environ.get("KUN_HOME", Path.home() / ".local/share/kun"))
VENDOR = INSTALL / "firstmate"
AGENTS = ("claude", "codex", "opencode")


class KunError(Exception):
    pass


def run(argv, cwd=None, env=None, check=True, capture=True, timeout=90):
    result = subprocess.run([str(x) for x in argv], cwd=cwd, env=env, text=True,
                            capture_output=capture, timeout=timeout)
    if check and result.returncode:
        raise KunError((result.stderr or result.stdout or f"Command failed: {argv[0]}").strip())
    return result


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n")
    temp.replace(path)


def project_root(path):
    path = Path(path).expanduser().resolve()
    if path.is_file():
        path = path.parent
    if not path.is_dir():
        raise KunError(f"Not a project directory: {path}")
    result = run(["git", "rev-parse", "--show-toplevel"], cwd=path, check=False)
    if result.returncode:
        raise KunError("This folder needs a Git repository with a first commit. Initialize Git and review/commit the intended files, then run kun again. No files were added or committed.")
    root = Path(result.stdout.strip()).resolve()
    if any(ord(char) < 32 or ord(char) == 127 for char in str(root)):
        raise KunError("Project paths with control characters are not supported")
    if root in {Path.home().resolve(), Path("/")}:
        raise KunError("Choose a specific project rather than your home or filesystem root")
    if run(["git", "rev-parse", "--verify", "HEAD"], cwd=root, check=False).returncode:
        raise KunError("Git is initialized, but this project needs its first commit before isolated workers can start")
    if root == VENDOR.resolve():
        raise KunError("Run kun from your application project, not the shared Firstmate checkout")
    return root


def identity(root):
    digest = hashlib.sha256(str(root).encode()).hexdigest()[:12]
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", root.name).strip("-").lower()[:32] or "project"
    return slug, digest, DATA / "projects" / f"{slug}-{digest}"


def safe_remote(value):
    if "://" in value:
        parts = urlsplit(value)
        return urlunsplit((parts.scheme, parts.netloc.rsplit("@", 1)[-1], parts.path, "", ""))
    return value


def detect(root):
    checks = []
    languages = []
    def add(kind, argv, source):
        candidate = {"kind": kind, "argv": argv, "source": source, "verified": False}
        if candidate not in checks:
            checks.append(candidate)
    if (root / "package.json").exists():
        data = json.loads((root / "package.json").read_text())
        manager = str(data.get("packageManager", "")).split("@", 1)[0]
        if manager not in {"npm", "pnpm", "yarn", "bun"}:
            manager = next((name for name, lock in (("pnpm", "pnpm-lock.yaml"), ("yarn", "yarn.lock"), ("bun", "bun.lock"), ("bun", "bun.lockb")) if (root / lock).exists()), "npm")
        for kind in ("build", "test", "lint", "typecheck", "check", "format"):
            script = data.get("scripts", {}).get(kind)
            if isinstance(script, str) and "no test specified" not in script.lower():
                add(kind, [manager, "run", kind], f"package.json scripts.{kind}")
        languages.append("JavaScript/TypeScript")
    pyproject = root / "pyproject.toml"
    if pyproject.exists() or (root / "requirements.txt").exists():
        languages.append("Python")
        metadata = tomllib.loads(pyproject.read_text()) if pyproject.exists() else {}
        text = pyproject.read_text() if pyproject.exists() else ""
        if (root / "requirements.txt").exists():
            text += (root / "requirements.txt").read_text()
        runner = ["uv", "run"] if (root / "uv.lock").exists() else (["poetry", "run"] if (root / "poetry.lock").exists() else [])
        if "pytest" in text.lower():
            add("test", [*runner, "python", "-m", "pytest"], "declared pytest tooling")
        if "ruff" in metadata.get("tool", {}):
            add("lint", [*runner, "ruff", "check", "."], "pyproject.toml tool.ruff")
    if (root / "CMakeLists.txt").exists():
        languages.append("C/C++ (CMake)")
        add("build", ["cmake", "--build", "build"], "CMakeLists.txt; configure a build directory first")
        if re.search(r"\b(enable_testing|include\s*\(\s*CTest)\b", (root / "CMakeLists.txt").read_text(), re.I):
            add("test", ["ctest", "--test-dir", "build", "--output-on-failure"], "CMake testing declaration; build first")
    if (root / "go.mod").exists():
        languages.append("Go")
        add("build", ["go", "build", "./..."], "go.mod")
        add("test", ["go", "test", "./..."], "go.mod")
    if (root / "Cargo.toml").exists():
        languages.append("Rust")
        add("build", ["cargo", "build"], "Cargo.toml")
        add("test", ["cargo", "test"], "Cargo.toml")
    for makefile in ("Makefile", "makefile"):
        if (root / makefile).exists():
            content = (root / makefile).read_text()
            for target in re.findall(r"^(build|test|lint|check|format)\s*:", content, re.M):
                if not any(item["kind"] == target for item in checks):
                    add(target, ["make", target], makefile + " target")
    origin = run(["git", "remote", "get-url", "origin"], cwd=root, check=False)
    branch = run(["git", "branch", "--show-current"], cwd=root).stdout.strip()
    dirty = bool(run(["git", "status", "--porcelain"], cwd=root).stdout.strip())
    return {"languages": languages, "checks": checks, "origin": safe_remote(origin.stdout.strip()) if origin.returncode == 0 else "",
            "branch": branch, "dirty": dirty,
            "instructions": [name for name in ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md") if (root / name).exists()]}


def environment(home):
    config = json.loads((home / "project.json").read_text())
    env = os.environ.copy()
    env.update({"FM_HOME": str(home), "FM_BACKEND": "tmux", "NM_HOME": str(DATA / "nm" / config["id"]),
                "FM_FLEET_PRUNE": "0", "KUN_LINKED_PROJECTS": "1", "NO_MISTAKES_TELEMETRY": "0", "NO_MISTAKES_NO_UPDATE_CHECK": "1",
                "KUN_INSTALL_ROOT": str(INSTALL), "KUN_HOME": str(DATA)})
    env["PATH"] = os.pathsep.join([str(INSTALL / "guards"), str(INSTALL / "toolchain/bin"),
                                   str(INSTALL / "toolchain/node_modules/.bin"), env.get("PATH", "")])
    return env


def ensure_installation():
    if not (VENDOR / "AGENTS.md").exists() or not (INSTALL / "installation.json").exists():
        raise KunError("The shared toolchain is missing. Re-run agentic/install.py from the setup source.")


def setup(root, agent=None, mode="auto"):
    ensure_installation()
    slug, digest, home = identity(root)
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (home / ".setup.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        existing = json.loads((home / "project.json").read_text()) if (home / "project.json").exists() else {}
        info = detect(root)
        selected_agent = agent or existing.get("agent") or "codex"
        install = json.loads((INSTALL / "installation.json").read_text())
        if selected_agent not in install.get("agents", {}):
            raise KunError(f"{selected_agent} CLI is unavailable; choose another with --agent")
        registry = home / "data/projects.md"
        registry_mode = None
        if registry.exists():
            # Native Firstmate may have changed the delivery mode since setup.
            for line in registry.read_text().splitlines():
                match = re.match(rf"^- {re.escape(slug)} \[(local-only|no-mistakes)(?=[\s\]+])", line)
                if match:
                    registry_mode = match[1]
        if mode == "auto":
            github = bool(re.match(r"(?:[^@]+@)?github\.com:", info["origin"]) or urlsplit(info["origin"]).hostname == "github.com")
            selected_mode = registry_mode or existing.get("mode") or ("no-mistakes" if github else "local-only")
        else:
            selected_mode = mode
        if selected_mode == "no-mistakes" and not info["origin"]:
            raise KunError("No Mistakes PR mode needs an origin remote. Use --mode local-only for a local project.")
        for directory in ("config", "data", "state", "projects"):
            (home / directory).mkdir(exist_ok=True)
        link = home / "projects" / slug
        if link.is_symlink():
            if link.resolve() != root:
                raise KunError("The project registration points elsewhere; refusing to replace it")
        elif link.exists():
            raise KunError("The project registration path is occupied; refusing to overwrite it")
        else:
            link.symlink_to(root, target_is_directory=True)
        config = {**existing, "schema": 1, "id": digest, "name": slug, "root": str(root), "home": str(home),
                  "agent": selected_agent, "mode": selected_mode, "detected": info,
                  "created": existing.get("created", date.today().isoformat())}
        write_json(home / "project.json", config)
        (home / "config/backend").write_text("tmux\n")
        (home / "config/claude-permission-mode").write_text("auto\n")
        write_json(home / "config/crew-dispatch.json", {"default": {"harness": selected_agent}})
        registry_lines = registry.read_text().splitlines() if registry.exists() else ["# Projects", ""]
        matching = [i for i, line in enumerate(registry_lines) if line.startswith(f"- {slug} [") or line.startswith(f"- {slug} - ")]
        entry = f"- {slug} [{selected_mode} branch=codex/] - Existing local project at {root} (added {config['created']})"
        if not matching:
            registry_lines.append(entry)
        elif mode != "auto":
            registry_lines[matching[0]] = entry
        registry.write_text("\n".join(registry_lines) + "\n")
        context = ["# Detected project context", "", f"Source: {root}", f"Languages: {', '.join(info['languages']) or 'not inferred'}",
                   f"Project instructions: {', '.join(info['instructions']) or 'none found'}", "",
                   "## Candidate checks — not yet executed", ""]
        context += [f"- {item['kind']}: `{shlex.join(item['argv'])}` — {item['source']}" for item in info["checks"]]
        if not info["checks"]:
            context.append("- No reliable build/test command was inferred. Inspect project documentation before choosing one.")
        context += ["", "Do not report these checks as passed until they have actually run.",
                    "Read existing project instructions. Do not replace them or commit unrelated changes."]
        (home / "data/project-context.md").write_text("\n".join(context) + "\n")
        captain = home / "data/captain.md"
        if not captain.exists():
            captain.write_text("# Working preferences\n\n"
                               "Use this home's registered delivery mode and harness. Never enable yolo merging.\n"
                               "Get my approval for merges. Keep tasks focused and show checks and evidence.\n"
                               "On initial onboarding, read data/project-context.md and the project's existing instructions.\n"
                               "Treat detected check commands as candidates until verified; ask only when the repository cannot resolve a required choice.\n"
                               "Do not replace global agent instructions or weaken the supplied harness permission controls.\n"
                               "Summarize each completed change in beginner-friendly terms: what changed, what I can do, how to use it, and what was checked.\n"
                               "Do not fetch, fast-forward, prune or otherwise change the registered source checkout as routine startup housekeeping.\n")
        env = environment(home)
        nm_home = Path(env["NM_HOME"])
        nm_home.mkdir(parents=True, exist_ok=True)
        nm_config = nm_home / "config.yaml"
        if not nm_config.exists():
            nm_config.write_text(f"agent: {selected_agent}\nagent_args_override:\n"
                                 "  claude: [--permission-mode, auto]\n"
                                 "  codex: [--sandbox, workspace-write]\n"
                                 "agent_path_override:\n"
                                 + "".join(f"  {name}: {json.dumps(str(INSTALL / 'guards' / name))}\n" for name in AGENTS)
                                 +
                                 "test:\n  evidence:\n    store_in_repo: false\n")
        elif agent:
            content = nm_config.read_text()
            content = re.sub(r"^agent: [^\n]+", f"agent: {selected_agent}", content, count=1, flags=re.M)
            nm_config.write_text(content)
        if selected_mode == "no-mistakes":
            if run(["git", "remote", "get-url", "no-mistakes"], cwd=root, check=False).returncode != 0:
                for base in (".agents", ".claude"):
                    skill = Path.home() / base / "skills/no-mistakes/SKILL.md"
                    backup = DATA / "backups" / "skills" / base / "SKILL.md"
                    if skill.exists() and not backup.exists():
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(skill, backup)
                print("Initializing the local No Mistakes gate (no code is pushed during setup).", file=sys.stderr)
                result = run(["no-mistakes", "init"], cwd=root, env=env, timeout=120)
                (home / "state/gate-init.log").write_text(result.stdout + result.stderr)
            # Require the registered gate to belong to this project's private NM_HOME.
            gate = run(["git", "remote", "get-url", "no-mistakes"], cwd=root).stdout.strip()
            if not Path(gate).expanduser().resolve().is_relative_to(nm_home.resolve()):
                raise KunError("This repository already has a No Mistakes gate outside Kun. It was preserved; use --mode local-only or explicitly migrate that gate before using Kun's PR mode.")
        return config


def summary(config):
    print(f"Project: {config['root']}\nAgent: {config['agent']}\nDelivery: {config['mode']} (merge approval required)\nWorkspace: {config['home']}")
    if config["detected"]["dirty"]:
        print("Existing uncommitted changes are preserved. Worker worktrees start from committed history.")
    for item in config["detected"]["checks"]:
        print(f"Candidate {item['kind']}: {shlex.join(item['argv'])}")


def primary_command(config):
    prompt = (f"Initialize or resume the Firstmate home at {config['home']} for registered project {config['name']}. "
              "Read data/project-context.md and existing project instructions. This opening request authorizes onboarding and an explanation only; "
              "do not invent a coding task or publish anything. Explain the detected setup, unresolved prerequisites, and how I can give you the first task. "
              "Preserve unrelated edits, require my approval for merges, and keep the configured permission controls.")
    agent = config["agent"]
    if agent == "claude":
        return [str(INSTALL / "guards/claude"), "--permission-mode", "default", prompt]
    if agent == "codex":
        return [str(INSTALL / "guards/codex"), prompt]
    return [str(INSTALL / "guards/opencode"), "--prompt", prompt]


def tmux_command(*args):
    socket = os.environ.get("KUN_TMUX_SOCKET")
    return ["tmux", *(["-L", socket] if socket else []), *args]


def launch(config, attach=True, preview=False):
    home = Path(config["home"])
    env = environment(home)
    command = primary_command(config)
    if preview:
        print(json.dumps({"cwd": str(VENDOR), "argv": command, "FM_HOME": str(home), "NM_HOME": env["NM_HOME"], "mode": config["mode"]}, indent=2))
        return
    session = "kun-" + config["name"][:20] + "-" + config["id"][:6]
    runner = [sys.executable, str(Path(__file__).resolve()), "_run", "--home", str(home)]
    exists = run(tmux_command("has-session", "-t", "=" + session), env=env, check=False).returncode == 0
    if not exists:
        args = tmux_command("new-session", "-d", "-s", session, "-n", "helm", "-c", str(VENDOR))
        for key in ("PATH", "FM_HOME", "FM_BACKEND", "NM_HOME", "KUN_INSTALL_ROOT", "KUN_HOME", "NO_MISTAKES_TELEMETRY", "NO_MISTAKES_NO_UPDATE_CHECK", "FM_FLEET_PRUNE", "KUN_LINKED_PROJECTS"):
            args += ["-e", key + "=" + env[key]]
        # Hold only our new pane until remain-on-exit is set, avoiding a race
        # when a harness immediately exits on a missing-login diagnostic.
        args += ["exec sleep 30"]
        run(args, env=env)
        run(tmux_command("set-option", "-w", "-t", session + ":helm", "remain-on-exit", "on"), env=env)
        run(tmux_command("respawn-pane", "-k", "-t", session + ":helm", "-c", str(VENDOR), shlex.join(runner)), env=env)
    else:
        dead = run(tmux_command("display-message", "-p", "-t", session + ":helm", "#{pane_dead}"), env=env).stdout.strip()
        if dead == "1":
            run(tmux_command("respawn-pane", "-t", session + ":helm", "-c", str(VENDOR), shlex.join(runner)), env=env)
    print("Firstmate session:", session)
    if attach:
        if not sys.stdin.isatty():
            print("Attach from a terminal: " + shlex.join(tmux_command("attach", "-t", session)))
            return
        if os.environ.get("TMUX"):
            run(tmux_command("switch-client", "-t", session), env=env)
        else:
            os.execvpe("tmux", tmux_command("attach-session", "-t", session), env)


def doctor():
    ensure_installation()
    env = os.environ.copy()
    env["PATH"] = os.pathsep.join([str(INSTALL / "toolchain/bin"), str(INSTALL / "toolchain/node_modules/.bin"), env.get("PATH", "")])
    missing = []
    for name in ("git", "node", "tmux", "gh", "treehouse", "no-mistakes", "gh-axi", "chrome-devtools-axi", "tasks-axi", "quota-axi", "lavish-axi"):
        path = shutil.which(name, path=env["PATH"])
        print(("OK      " if path else "MISSING ") + name)
        if not path:
            missing.append(name)
    agents = json.loads((INSTALL / "installation.json").read_text()).get("agents", {})
    print("Installed assistants: " + ", ".join(agents))
    result = run(["gh", "auth", "status"], env=env, check=False, timeout=30)
    print("GitHub: " + ("authentication verified" if result.returncode == 0 else "not verified; run gh auth login if needed"))
    if "codex" in agents:
        login = run([agents["codex"], "login", "status"], env=env, check=False, timeout=30)
        print("Codex: " + ("authentication verified" if login.returncode == 0 else "not verified; run codex login if needed"))
    print("No model request was made. Other assistants keep their own sign-in settings.")
    if missing:
        raise KunError("Missing shared tools: " + ", ".join(missing))


def main(argv=None):
    values = list(sys.argv[1:] if argv is None else argv)
    actions = {"start", "setup", "init", "status", "doctor", "exec", "check", "_run"}
    if not values or values[0].startswith("-"):
        if values and values[0] in {"--help", "-h"}:
            values = ["--help"]
        else:
            values.insert(0, "start")
    elif values[0] not in actions:
        values = ["start", "--project", values[0], *values[1:]]
    parser = argparse.ArgumentParser(description="Set up or reopen Kun's project-scoped Firstmate workflow")
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("start", "setup", "init", "status", "exec", "check"):
        command = sub.add_parser(action)
        command.add_argument("--project", "-C", default=".")
        if action in {"start", "setup", "init"}:
            command.add_argument("--agent", choices=AGENTS)
            command.add_argument("--mode", choices=("auto", "local-only", "no-mistakes"), default="auto")
        if action == "start":
            command.add_argument("--print", dest="preview", action="store_true", help="Prepare setup and print launch details without calling a model")
            command.add_argument("--no-attach", action="store_true")
        if action == "status":
            command.add_argument("--json", action="store_true")
        if action == "exec":
            command.add_argument("command", nargs=argparse.REMAINDER)
        if action == "check":
            command.add_argument("--kind", default="test", choices=("test", "build", "lint", "typecheck", "check", "format"))
            command.add_argument("--run", action="store_true", help="Execute the detected project command")
    sub.add_parser("doctor")
    internal = sub.add_parser("_run", help=argparse.SUPPRESS)
    internal.add_argument("--home", required=True)
    args = parser.parse_args(values)
    if args.action == "doctor":
        doctor()
        return
    if args.action == "_run":
        home = Path(args.home).resolve()
        config = json.loads((home / "project.json").read_text())
        os.chdir(VENDOR)
        command = primary_command(config)
        os.execvpe(command[0], command, environment(home))
    root = project_root(args.project)
    _, _, home = identity(root)
    if args.action in {"start", "setup", "init"}:
        config = setup(root, args.agent, args.mode)
        if args.action == "start" and args.preview:
            launch(config, preview=True)
        else:
            summary(config)
            if args.action == "start":
                launch(config, attach=not args.no_attach)
        return
    if not (home / "project.json").exists():
        raise KunError("This project is not set up yet. Run kun setup here first.")
    config = json.loads((home / "project.json").read_text())
    if args.action == "status":
        print(json.dumps(config, indent=2)) if args.json else summary(config)
    elif args.action == "exec":
        command = args.command
        if command and command[0] == "--":
            command = command[1:]
        if not command:
            raise KunError("Example: kun exec -- no-mistakes doctor")
        os.chdir(root)
        os.execvpe(command[0], command, environment(home))
    elif args.action == "check":
        checks = [item for item in config["detected"]["checks"] if item["kind"] == args.kind]
        if not checks:
            raise KunError("No reliable command was inferred for this check; inspect the project's documented commands")
        for check in checks:
            print(shlex.join(check["argv"]), flush=True)
            if args.run:
                result = run(check["argv"], cwd=root, env=environment(home), capture=False, timeout=None, check=False)
                write_json(home / "state/last-check.json", {"kind": args.kind, "argv": check["argv"], "exit_code": result.returncode, "timestamp": time.time()})
                if result.returncode:
                    raise KunError(f"{args.kind} failed (exit {result.returncode}); recorded in state/last-check.json")
        if not args.run:
            print("Preview only. Add --run to execute project code.")


if __name__ == "__main__":
    try:
        main()
    except (KunError, ValueError, OSError, subprocess.TimeoutExpired) as error:
        print("kun:", error, file=sys.stderr)
        sys.exit(1)

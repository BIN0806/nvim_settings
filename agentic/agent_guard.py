#!/usr/bin/env python3
"""Private CLI adapters: retain the installed harnesses' permission controls."""
import json
import os
from pathlib import Path
import sys


def codex_args(args, home):
    result = []
    index = 0
    while index < len(args):
        item = args[index]
        if item in {"--dangerously-bypass-approvals-and-sandbox", "--dangerously-bypass-hook-trust", "--yolo", "--full-auto", "--approve-for-me"}:
            index += 1
            continue
        if item in {"--sandbox", "-s", "--ask-for-approval", "-a"}:
            index += 2
            continue
        if item.startswith(("--sandbox=", "--ask-for-approval=")):
            index += 1
            continue
        if (item.startswith("-s") or item.startswith("-a")) and not item.startswith("--") and len(item) > 2:
            index += 1
            continue
        if item in {"--config", "-c"} and index + 1 < len(args):
            key = args[index + 1].split("=", 1)[0].strip()
            if key in {"approval_policy", "sandbox_mode"} or key.startswith("sandbox_workspace_write."):
                index += 2
                continue
        attached = item.removeprefix("--config=") if item.startswith("--config=") else (item[2:] if item.startswith("-c") and not item.startswith("--") and len(item) > 2 else "")
        key = attached.split("=", 1)[0].strip()
        if key in {"approval_policy", "sandbox_mode"} or key.startswith("sandbox_workspace_write."):
            index += 1
            continue
        result.append(item)
        index += 1
    prefix = ["--sandbox", "workspace-write", "-c", 'approval_policy="on-request"']
    if home:
        prefix += ["--add-dir", home]
    return prefix + result


def claude_args(args):
    result = []
    index = 0
    while index < len(args):
        item = args[index]
        if item in {"--dangerously-skip-permissions", "--allow-dangerously-skip-permissions"}:
            result += ["--permission-mode", "auto"]
        elif item == "--permission-mode" and index + 1 < len(args):
            value = args[index + 1]
            result += [item, "auto" if value in {"bypassPermissions", "dontAsk"} else value]
            index += 1
        elif item.startswith("--permission-mode="):
            value = item.split("=", 1)[1]
            result += ["--permission-mode", "auto" if value in {"bypassPermissions", "dontAsk"} else value]
        else:
            result.append(item)
        index += 1
    return result


def main():
    prefix = Path(os.environ.get("KUN_INSTALL_ROOT", Path(__file__).resolve().parents[1]))
    name = Path(sys.argv[0]).name
    record = json.loads((prefix / "installation.json").read_text())
    binary = record.get("agents", {}).get(name)
    if not binary or not Path(binary).exists():
        raise SystemExit(f"kun: {name} is not installed; select another installed agent")
    args = sys.argv[1:]
    env = os.environ.copy()
    probe = any(a in {"--help", "--version", "-h", "-V"} for a in args) or (args and args[0] in {"auth", "login", "logout", "help", "completion"})
    if not probe:
        if name == "codex":
            args = codex_args(args, env.get("FM_HOME"))
        elif name == "claude":
            args = claude_args(args)
        elif name == "opencode":
            content = json.loads(env.get("OPENCODE_CONFIG_CONTENT", "{}"))
            # Preserve model/effort settings but remove the upstream blanket allow.
            content["permission"] = {"*": "ask"}
            env["OPENCODE_CONFIG_CONTENT"] = json.dumps(content)
            env.pop("OPENCODE_PERMISSION", None)
    os.execve(binary, [binary, *args], env)


if __name__ == "__main__":
    main()

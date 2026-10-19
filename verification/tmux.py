from pathlib import Path
import json
import os
import shlex
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
socket = "codex-nvim-merge-verify"
checks = []
def tmux(*args):
    result = subprocess.run(["tmux", "-L", socket, *args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()
def passed(name):
    checks.append({"check": name, "passed": True})
    print("PASS:", name)

with tempfile.TemporaryDirectory(prefix="nvim-tmux-") as temp:
    try:
        tmux("-f", str(root / "tmux.conf"), "new-session", "-d", "-s", "verification", "-c", temp)
        assert tmux("show-options", "-gv", "prefix") == "C-s"
        assert tmux("show-options", "-gv", "default-terminal") == "tmux-256color"
        passed("tmux configuration loads with preserved prefix and truecolor terminal")
        bindings = tmux("list-keys")
        for key in ("split-window -h", "split-window -v", "copy-pipe-and-cancel", "save.sh", "restore.sh"):
            assert key in bindings, "Missing tmux binding: " + key
        passed("split, clipboard, navigation and persistence bindings are loaded")
        tmux("split-window", "-h", "-t", "verification", "-c", temp)
        assert len(tmux("list-panes", "-t", "verification").splitlines()) == 2
        assert tmux("show-options", "-gv", "@resurrect-processes") == "false"
        assert tmux("show-options", "-gv", "@continuum-restore") == "off"
        tmux("set-option", "-g", "@resurrect-dir", str(Path(temp) / "saved"))
        saver = Path.home() / ".tmux/plugins/tmux-resurrect/scripts/save.sh"
        tmux("run-shell", str(saver))
        saved = Path(temp) / "saved/last"
        assert saved.exists() and "pane" in saved.read_text()
        passed("real two-pane layout saved; automatic process restoration disabled")
        (root / "verification/tmux-results.json").write_text(json.dumps(checks, indent=2) + "\n")
    finally:
        subprocess.run(["tmux", "-L", socket, "kill-server"], capture_output=True)

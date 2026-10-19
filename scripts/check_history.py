#!/usr/bin/env python3
"""Require a staged settings-change log entry when committing settings."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
changed = subprocess.check_output(["git", "diff", "--cached", "--name-only", "-z"], cwd=ROOT).decode().split("\0")
settings = {"init.lua", "lazy-lock.json", "profile.json", "tmux.conf", ".stylua.toml"}
has_settings = any(path in settings or path.startswith(("lua/", "agentic/")) for path in changed)
if has_settings and "Documentation.md" not in changed:
    raise SystemExit("Settings changed: stage a Change log entry in Documentation.md describing the change, usage, validation and restore notes before committing.")

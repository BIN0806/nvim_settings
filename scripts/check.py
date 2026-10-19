#!/usr/bin/env python3
"""Check the settings snapshot without loading plugins or starting agents."""
import ast
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / "agentic").glob("*.py"):
    ast.parse(path.read_text(), filename=str(path))
for path in (ROOT / "scripts").glob("*.py"):
    ast.parse(path.read_text(), filename=str(path))
for relative in ("lazy-lock.json", "profile.json", "agentic/toolchain-lock.json"):
    json.loads((ROOT / relative).read_text())
print("PASS: Python sources and JSON records parse", flush=True)
subprocess.run([shutil.which("python3") or "python3", str(ROOT / "scripts/check_documentation.py")], cwd=ROOT, check=True)
if not shutil.which("nvim"):
    raise SystemExit("Install Neovim before checking Lua settings")
subprocess.run(["nvim", "--headless", "-u", "NONE", "-i", "NONE", "-n", "-l", str(ROOT / "scripts/check.lua")], cwd=ROOT, check=True)

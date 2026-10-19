#!/usr/bin/env python3
"""Install the reviewed Kun launcher and official tools in a private user prefix."""
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import shlex
import subprocess
import sys
import tarfile
from urllib.request import Request, urlopen
import overlay

SOURCE = Path(__file__).resolve().parent
PREFIX = Path.home() / ".local/share/kun"
FIRSTMATE_COMMIT = "45dd50a5e12bc3f5e009a4e18fa35ce7f7a71681"
PACKAGES = {
    "gh-axi": "0.1.43", "chrome-devtools-axi": "0.1.44",
    "tasks-axi": "0.2.6", "quota-axi": "0.1.64", "lavish-axi": "0.1.90",
}


def download(url):
    with urlopen(Request(url, headers={"User-Agent": "kun-local-setup"}), timeout=120) as response:
        return response.read()


def binary(repo, tag):
    machine = {"arm64": "arm64", "x86_64": "amd64"}[platform.machine()]
    system = {"Darwin": "darwin", "Linux": "linux"}[platform.system()]
    name = f"{repo}-{tag}-{system}-{machine}.tar.gz"
    base = f"https://github.com/kunchenguid/{repo}/releases/download/{tag}"
    checksums = download(base + "/checksums.txt").decode()
    expected = next(line.split()[0] for line in checksums.splitlines() if line.split()[-1].lstrip("*") == name)
    payload = download(base + "/" + name)
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected:
        raise RuntimeError(f"Checksum mismatch for {name}")
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        member = next(m for m in archive.getmembers() if Path(m.name).name == repo and m.isfile())
        content = archive.extractfile(member).read()
    target = PREFIX / "toolchain/bin" / repo
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix(".new")
    temp.write_bytes(content)
    temp.chmod(0o755)
    temp.replace(target)
    return {"version": tag, "archive": name, "sha256": actual, "source": base}


def main():
    PREFIX.mkdir(parents=True, exist_ok=True, mode=0o700)
    PREFIX.chmod(0o700)
    record_path = PREFIX / "installation.json"
    record = json.loads(record_path.read_text()) if record_path.exists() else {}
    vendor = PREFIX / "firstmate"
    if not vendor.exists():
        subprocess.run(["git", "clone", "--depth=1", "https://github.com/kunchenguid/firstmate.git", str(vendor)], check=True)
    head = subprocess.check_output(["git", "-C", str(vendor), "rev-parse", "HEAD"], text=True).strip()
    if head != FIRSTMATE_COMMIT:
        dirty = subprocess.check_output(["git", "-C", str(vendor), "status", "--porcelain"], text=True)
        if dirty:
            raise RuntimeError("Existing Firstmate checkout has changes; refusing to reset it")
        subprocess.run(["git", "-C", str(vendor), "fetch", "--depth=1", "origin", FIRSTMATE_COMMIT], check=True)
        subprocess.run(["git", "-C", str(vendor), "checkout", "-B", "main", FIRSTMATE_COMMIT], check=True)
    record["firstmate"] = {"commit": FIRSTMATE_COMMIT, "source": "https://github.com/kunchenguid/firstmate"}
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    for name, version in (("treehouse", "v3.1.4"), ("no-mistakes", "v1.84.0")):
        if record.get(name, {}).get("version") != version or not (PREFIX / "toolchain/bin" / name).exists():
            record[name] = binary(name, version)
            record_path.write_text(json.dumps(record, indent=2) + "\n")
        print(f"Installed {name} {version} (official release checksum verified)", flush=True)
    toolchain = PREFIX / "toolchain"
    if record.get("npm_packages") != PACKAGES:
        subprocess.run(["npm", "install", "--prefix", str(toolchain), "--no-audit", "--no-fund",
                        *[f"{name}@{version}" for name, version in PACKAGES.items()]], check=True)
        record["npm_packages"] = PACKAGES
    launcher = PREFIX / "launcher"
    launcher.mkdir(exist_ok=True)
    for name in ("kun.py", "agent_guard.py"):
        source = SOURCE / name
        if source.exists():
            shutil.copy2(source, launcher / name)
            (launcher / name).chmod(0o755)
    entry = Path.home() / ".local/bin/kun"
    entry.parent.mkdir(parents=True, exist_ok=True)
    if entry.exists() or entry.is_symlink():
        if entry.resolve() != (launcher / "kun.py").resolve():
            raise RuntimeError(f"{entry} already exists and belongs to another command")
    else:
        entry.symlink_to(launcher / "kun.py")
    guards = PREFIX / "guards"
    guards.mkdir(exist_ok=True)
    for name in ("claude", "codex", "opencode"):
        original = shutil.which(name)
        if original and not str(Path(original).resolve()).startswith(str(PREFIX)):
            record.setdefault("agents", {})[name] = str(Path(original).resolve())
        link = guards / name
        if not link.exists() and not link.is_symlink():
            link.symlink_to(launcher / "agent_guard.py")
    # Resolve the package runtimes outside any project virtual environment.
    python = Path("/opt/homebrew/bin/python3")
    if not python.exists():
        python = Path(sys.executable)
    node = Path("/opt/homebrew/bin/node")
    if not node.exists():
        node = Path(shutil.which("node"))
    for name in ("kun.py", "agent_guard.py"):
        target = launcher / name
        target.write_text(f"#!{python}\n" + target.read_text().split("\n", 1)[1])
    for name in PACKAGES:
        target = toolchain / "bin" / name
        target.write_text("#!/bin/sh\nexec " + shlex.quote(str(node)) + " " +
                          shlex.quote(str(toolchain / "node_modules/.bin" / name)) + ' "$@"\n')
        target.chmod(0o755)
    record["runtimes"] = {"python": str(python), "node": str(node)}
    record["overlays"] = overlay.apply(vendor, PREFIX, FIRSTMATE_COMMIT, record.get("overlays", {}))
    record["launcher"] = str(launcher / "kun.py")
    record["prefix"] = str(PREFIX)
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    (SOURCE / "installation.json").write_text(json.dumps(record, indent=2) + "\n")
    print("Kun launcher/toolchain installed in", PREFIX)


if __name__ == "__main__":
    main()

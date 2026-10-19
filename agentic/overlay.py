"""Small, recorded integration changes to the pinned private Firstmate copy."""
import hashlib
from pathlib import Path
import shlex
import subprocess


def render(relative, original, prefix):
    content = original
    if relative == "bin/fm-spawn.sh":
        # Absolute paths survive login shells that rebuild PATH in worker panes.
        for name, marker, expected in (("claude", "claude __CLAUDEPERMFLAG__", 1),
                                      ("codex", "codex __MODELFLAG__", 2),
                                      ("opencode", "opencode __MODELFLAG__", 1)):
            if content.count(marker) != expected:
                raise RuntimeError(f"Firstmate launch template changed: {marker}")
            word = shlex.quote(str(prefix / "guards" / name)).replace("'", "'\\''")
            content = content.replace(marker, word + marker[len(name):])
    elif relative == "bin/fm-bootstrap.sh":
        marker = "fleet_sync() {\n"
        if content.count(marker) != 1:
            raise RuntimeError("Firstmate fleet_sync integration point changed")
        content = content.replace(marker, marker +
                                  '  # Kun registers the actual source checkout; startup must not update it.\n'
                                  '  [ "${KUN_LINKED_PROJECTS:-0}" != 1 ] || return 0\n', 1)
    else:
        raise RuntimeError(f"Unknown integration overlay: {relative}")
    return content


def apply(vendor, prefix, commit, previous):
    records = {}
    for relative in ("bin/fm-spawn.sh", "bin/fm-bootstrap.sh"):
        path = vendor / relative
        original = subprocess.check_output(["git", "-C", str(vendor), "show", f"{commit}:{relative}"], text=True)
        desired = render(relative, original, prefix)
        current = path.read_text()
        old_hash = previous.get(relative, {}).get("sha256")
        if current not in {original, desired} and hashlib.sha256(current.encode()).hexdigest() != old_hash:
            raise RuntimeError(f"Unrecognized local changes in {path}; preserved rather than overwritten")
        if current != desired:
            path.write_text(desired)
        subprocess.run(["bash", "-n", str(path)], check=True)
        records[relative] = {"sha256": hashlib.sha256(desired.encode()).hexdigest()}
    return records

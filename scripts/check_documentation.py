#!/usr/bin/env python3
"""Validate the single user guide and its local navigation without network calls."""
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def visible_lines(text):
    """Skip code fences so the embedded project template is not a second guide."""
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield line
    if fence is not None:
        raise ValueError("Documentation.md contains an unclosed code fence")


def anchors(text):
    result = set()
    for line in visible_lines(text):
        heading = re.match(r"^#{1,6}\s+(.+)$", line)
        if heading:
            slug = re.sub(r"[^\w\- ]", "", heading[1].strip().lower()).replace(" ", "-")
            if slug in result:
                raise ValueError(f"Duplicate documentation heading: {heading[1]}")
            result.add(slug)
    return result


def main():
    document = ROOT / "Documentation.md"
    text = document.read_text()
    lines = list(visible_lines(text))
    ids = anchors(text)
    top = [line[3:] for line in lines if line.startswith("## ") and line != "## Contents"]
    if not top or top[-1] != "Final installed stack" or "Change log" not in top:
        raise ValueError("Keep the Change log and the final stack as the last category")
    for source in (document, ROOT / "AGENTS.md"):
        content = "\n".join(visible_lines(source.read_text()))
        for destination in re.findall(r"\]\(([^)]+)\)", content):
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc:
                continue
            target = source.parent / unquote(parsed.path) if parsed.path else source
            if not target.is_file():
                raise ValueError(f"Broken file link in {source.name}: {destination}")
            if parsed.fragment and target.resolve() == document.resolve() and unquote(parsed.fragment) not in ids:
                raise ValueError(f"Broken section link in {source.name}: {destination}")
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=ROOT
    ).decode().split("\0")
    extra = sorted({path for path in paths if path.endswith(".md") and (ROOT / path).is_file()
                    and path not in {"Documentation.md", "AGENTS.md"}})
    if extra:
        raise ValueError("Merge user documentation into Documentation.md: " + ", ".join(extra))
    print(f"PASS: one user guide, {len(top)} categories, unique headings and working local links/anchors")


if __name__ == "__main__":
    main()

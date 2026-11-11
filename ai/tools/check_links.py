#!/usr/bin/env python3
"""Link walk for the repo's Markdown: every relative [text](target) must resolve.

Only Markdown link syntax counts. Code such as `int(x)` or `a[i](y)` in a fenced
block or inline code is not a link, so those spans are skipped first.

Usage: python3 ai/tools/check_links.py [ROOT]   (default: the repo root). Exit 1 if any link is broken.
"""
import os
import re
import sys

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def links_in(path):
    """Yields (line number, target) for every Markdown link outside code."""
    in_fence = False
    with open(path, encoding="utf-8") as fh:
        for number, line in enumerate(fh, 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            text = INLINE_CODE.sub("", line)
            for match in LINK.finditer(text):
                yield number, match.group(1)


def check(root):
    broken = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            for number, target in links_in(path):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_path = target.split("#", 1)[0]
                if not os.path.exists(os.path.normpath(os.path.join(dirpath, target_path))):
                    broken.append((os.path.relpath(path, root), number, target))
    return broken


def main(argv):
    root = os.path.abspath(argv[1] if len(argv) > 1 else os.path.join(os.path.dirname(__file__), "..", ".."))
    broken = check(root)
    for path, number, target in broken:
        print("%s:%d: broken link to %s" % (path, number, target))
    if not broken:
        print("all relative links resolve")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

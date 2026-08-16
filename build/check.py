#!/usr/bin/env python3
"""
APFC RT Manual - quality gate.

Run after every authoring session, before building PDFs:

    python3 build/check.py

Checks each chapter in src/ for:
  1. Question numbering contiguous from 1
  2. An answer row for every question, contiguous from 1
  3. Answer key spread across (a)(b)(c)(d) reasonably balanced - a key where one
     letter never appears lets a candidate score by elimination and trains the
     wrong instinct
  4. Section headings numbered contiguously from 0 - catches gaps introduced by
     restructuring
  5. No codepoints in the built HTML that the installed font cannot render

Exits non-zero if anything fails, so it can gate a commit.
Stdlib only.
"""

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DOCS = ROOT / "docs"

# Noto Sans is the only installed family; these have no glyph in it and are
# substituted by build.py on the way out. Any survivor in docs/ is a bug.
UNRENDERABLE = {0x2605, 0x2606, 0x2192, 0x2190, 0x2191, 0x2193, 0x2282, 0x2248, 0x2260}

Q = re.compile(r"\*\*Q(\d+)\.\*\*")
ANS = re.compile(r"^\|\s*(\d+)\s*\|\s*([a-d])\s*\|", re.M)
H2 = re.compile(r"^## (\d+)\.", re.M)


def check_chapter(path):
    """Returns (list_of_failures, list_of_notes)."""
    fails, notes = [], []
    text = path.read_text(encoding="utf-8")
    name = path.name

    qs = sorted(int(m) for m in Q.findall(text))
    key = {int(n): l for n, l in ANS.findall(text)}

    if not qs:
        notes.append(f"{name}: no questions (index or front matter?)")
        return fails, notes

    if qs != list(range(1, len(qs) + 1)):
        missing = sorted(set(range(1, max(qs) + 1)) - set(qs))
        fails.append(f"{name}: question numbering not contiguous, missing {missing}")

    ans_nums = sorted(key)
    if ans_nums != qs:
        fails.append(f"{name}: questions {len(qs)} but answer rows {len(key)}; "
                     f"missing keys {sorted(set(qs) - set(ans_nums))}")

    spread = Counter(key.values())
    for letter in "abcd":
        spread.setdefault(letter, 0)
    counts = {k: spread[k] for k in "abcd"}
    lo, hi = min(counts.values()), max(counts.values())
    if lo == 0:
        fails.append(f"{name}: answer key never uses ({min(counts, key=counts.get)}) - {counts}")
    elif hi - lo > max(2, len(qs) // 8):
        fails.append(f"{name}: answer key badly skewed {counts}")
    else:
        notes.append(f"{name}: {len(qs)} questions, key {counts}")

    secs = [int(m) for m in H2.findall(text)]
    if secs:
        expected = list(range(secs[0], secs[0] + len(secs)))
        if secs != expected:
            fails.append(f"{name}: section numbering gap - found {secs}")

    html = DOCS / path.relative_to(SRC).with_suffix(".html")
    if html.exists():
        bad = Counter(ch for ch in html.read_text(encoding="utf-8")
                      if ord(ch) in UNRENDERABLE)
        if bad:
            fails.append(f"{name}: unrenderable glyphs survived into HTML: "
                         f"{ {c: n for c, n in bad.items()} }")
    else:
        notes.append(f"{name}: no built HTML yet - run build/build.py")

    return fails, notes


def main():
    if not SRC.exists():
        print("no src/ directory", file=sys.stderr)
        return 1

    all_fails, all_notes = [], []
    for path in sorted(SRC.rglob("*.md")):
        f, n = check_chapter(path)
        all_fails += f
        all_notes += n

    for n in all_notes:
        print(f"  ok   {n}")
    for f in all_fails:
        print(f"  FAIL {f}")

    print()
    if all_fails:
        print(f"{len(all_fails)} failure(s)")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

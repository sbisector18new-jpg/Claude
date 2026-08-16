#!/usr/bin/env python3
"""
APFC RT Manual - build tool.

Converts the Markdown master manuscript in src/ into styled, print-ready HTML in docs/.

Why HTML and not PDF: this sandbox has no PDF toolchain (no pandoc, weasyprint,
wkhtmltopdf or LaTeX) and PyPI is blocked, so reportlab/weasyprint cannot be installed.
The HTML output is therefore built to print cleanly to PDF from any browser
(Ctrl/Cmd-P -> Save as PDF), which preserves the "src/ is the source of truth"
convention: PDFs are always regenerated from src/, never hand-edited.

Stdlib only. No dependencies.

Usage:
    python3 build/build.py              # build everything in src/
    python3 build/build.py src/file.md  # build one file
"""

import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
CSS = Path(__file__).resolve().parent / "style.css"

# Callout block types -> CSS class. The source supplies the full heading text.
CALLOUT_TYPES = {
    "must-master", "high-yield", "know", "optional", "trap", "think",
    "memory", "jargon", "beginner", "why", "plain", "action", "note",
    "check", "session", "world", "important",
}


# ---------------------------------------------------------------- inline

def _slug(text):
    s = re.sub(r"<[^>]+>", "", text)
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-{2,}", "-", s) or "section"


# The only font family installed in this environment is Noto Sans, which has no
# glyph for these codepoints - they would print as blank boxes. The Markdown
# sources keep the proper characters (they read correctly everywhere else); the
# substitution happens only on the way out to HTML/PDF.
GLYPHS = {
    "\u2192": "&#187;",        # -> becomes a right guillemet
    "\u2190": "&#171;",        # <- becomes a left guillemet
    "\u2191": "(+)",           # up arrow
    "\u2193": "(&#8722;)",     # down arrow, using the available minus sign
    "\u2282": "part of",       # subset
    "\u2248": "about",         # approximately
    "\u2260": "is not",        # not equal
    "\u2265": "&gt;=",         # greater than or equal
    "\u2264": "&lt;=",         # less than or equal
    "\u221a": "sqrt",          # radical
    "\u221e": "infinity",      # infinity
    "\u2211": "\u03a3",        # n-ary summation -> Greek capital sigma, which IS available
}
# Verified present in Noto Sans and passed through untouched: Greek sigma, capital
# sigma, mu and rho; the superscript two; plus-minus; multiplication sign; the
# rupee sign; em and en dashes; middle dot; section sign; minus sign; ellipsis.

# Star ratings are drawn as CSS shapes rather than substituted, because the
# priority system is load-bearing and needs to stay visually scannable.
STAR_RUN = re.compile(r"[\u2605\u2606]{2,5}")


def _stars(text):
    def rep(m):
        run = m.group(0)
        on = run.count("\u2605")
        cells = "".join(
            f'<i class="{"on" if i < on else "off"}"></i>' for i in range(len(run))
        )
        return (f'<span class="rate" role="img" '
                f'aria-label="priority {on} of {len(run)}">{cells}</span>')
    return STAR_RUN.sub(rep, text)


def inline(text):
    """Inline formatting. Code spans are protected before other rules run."""
    stash = []

    def _keep(m):
        stash.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(stash) - 1}\x00"

    text = re.sub(r"`([^`]+)`", _keep, text)
    text = html.escape(text, quote=False)

    # links before emphasis so URLs with underscores survive
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        text,
    )
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", text)
    text = text.replace(" -- ", " &mdash; ")

    # glyph fallbacks last, so code spans (already stashed) keep their originals
    text = _stars(text)
    for ch, repl in GLYPHS.items():
        text = text.replace(ch, repl)

    for i, frag in enumerate(stash):
        text = text.replace(f"\x00{i}\x00", frag)
    return text


# ---------------------------------------------------------------- blocks

class Builder:
    def __init__(self):
        self.out = []
        self.toc = []

    def emit(self, s):
        self.out.append(s)

    # -- tables ---------------------------------------------------

    @staticmethod
    def _is_sep(line):
        return bool(re.fullmatch(r"\|[\s:|-]+\|", line.strip())) and "-" in line

    @staticmethod
    def _cells(line):
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [c.strip() for c in line.split("|")]

    def table(self, lines, caption=None):
        head = self._cells(lines[0])
        aligns = []
        for spec in self._cells(lines[1]):
            if spec.startswith(":") and spec.endswith(":"):
                aligns.append("center")
            elif spec.endswith(":"):
                aligns.append("right")
            else:
                aligns.append("left")
        while len(aligns) < len(head):
            aligns.append("left")

        self.emit('<div class="tw"><table>')
        self.emit("<thead><tr>" + "".join(
            f'<th style="text-align:{aligns[i]}">{inline(c)}</th>'
            for i, c in enumerate(head)
        ) + "</tr></thead><tbody>")

        for row in lines[2:]:
            cells = self._cells(row)
            tds = []
            for i, c in enumerate(cells):
                a = aligns[i] if i < len(aligns) else "left"
                tds.append(f'<td style="text-align:{a}">{inline(c)}</td>')
            self.emit("<tr>" + "".join(tds) + "</tr>")

        self.emit("</tbody></table>")
        if caption:
            self.emit(f'<p class="cap">{inline(caption)}</p>')
        self.emit("</div>")

    # -- lists ----------------------------------------------------

    def lists(self, items):
        """items: list of (indent, ordered, text). Nested via 2-space indents."""
        stack = []
        for indent, ordered, text in items:
            depth = indent // 2
            while len(stack) > depth + 1:
                self.emit(f"</li></{stack.pop()}>")
            if len(stack) == depth + 1:
                if stack[-1] != ("ol" if ordered else "ul"):
                    self.emit(f"</li></{stack.pop()}>")
                    tag = "ol" if ordered else "ul"
                    self.emit(f"<{tag}>")
                    stack.append(tag)
                else:
                    self.emit("</li>")
            else:
                tag = "ol" if ordered else "ul"
                self.emit(f"<{tag}>")
                stack.append(tag)
            self.emit(f"<li>{inline(text)}")
        while stack:
            self.emit(f"</li></{stack.pop()}>")

    # -- main loop ------------------------------------------------

    def run(self, lines):
        i = 0
        n = len(lines)
        while i < n:
            raw = lines[i]
            line = raw.rstrip()
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            # page break
            if stripped == r"\pagebreak":
                self.emit('<div class="pagebreak"></div>')
                i += 1
                continue

            # TOC placeholder
            if stripped == "[[TOC]]":
                self.emit("\x01TOC\x01")
                i += 1
                continue

            # horizontal rule
            if re.fullmatch(r"-{3,}|\*{3,}", stripped):
                self.emit("<hr>")
                i += 1
                continue

            # callout block
            m = re.match(r"^:::\s*([a-z-]+)\s*(?:\|\s*(.*))?$", stripped)
            if m:
                kind = m.group(1)
                title = (m.group(2) or "").strip()
                cls = kind if kind in CALLOUT_TYPES else "note"
                body = []
                i += 1
                while i < n and lines[i].strip() != ":::":
                    body.append(lines[i])
                    i += 1
                i += 1  # closing :::
                self.emit(f'<aside class="cal {cls}">')
                if title:
                    self.emit(f'<p class="cal-h">{inline(title)}</p>')
                inner = Builder()
                inner.run(body)
                self.emit("".join(inner.out))
                self.emit("</aside>")
                continue

            # headings
            m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                sid = _slug(text)
                if level in (2, 3):
                    self.toc.append((level, text, sid))
                self.emit(f'<h{level} id="{sid}">{inline(text)}</h{level}>')
                i += 1
                continue

            # blockquote
            if stripped.startswith(">"):
                body = []
                while i < n and lines[i].strip().startswith(">"):
                    body.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                inner = Builder()
                inner.run(body)
                self.emit(f"<blockquote>{''.join(inner.out)}</blockquote>")
                continue

            # table
            if stripped.startswith("|") and i + 1 < n and self._is_sep(lines[i + 1]):
                block = []
                while i < n and lines[i].strip().startswith("|"):
                    block.append(lines[i])
                    i += 1
                caption = None
                if i < n and lines[i].strip().startswith("^ "):
                    caption = lines[i].strip()[2:]
                    i += 1
                self.table(block, caption)
                continue

            # list
            m = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", raw)
            if m:
                items = []
                while i < n:
                    mm = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", lines[i])
                    if not mm:
                        if lines[i].strip() and items and lines[i].startswith("   "):
                            # continuation of previous item
                            ind, ordr, txt = items[-1]
                            items[-1] = (ind, ordr, txt + " " + lines[i].strip())
                            i += 1
                            continue
                        break
                    indent = len(mm.group(1))
                    ordered = not mm.group(2) in ("-", "*")
                    items.append((indent, ordered, mm.group(3)))
                    i += 1
                self.lists(items)
                continue

            # paragraph
            para = []
            while i < n and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|:::|\||>|\s*([-*]|\d+[.)])\s|\\pagebreak|\[\[TOC\]\]|-{3,}$)",
                lines[i].strip()
            ):
                para.append(lines[i].strip())
                i += 1
            if para:
                self.emit(f"<p>{inline(' '.join(para))}</p>")
            else:
                i += 1


# ---------------------------------------------------------------- document

def front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for ln in text[3:end].strip().splitlines():
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    meta[k.strip()] = v.strip()
            text = text[end + 4:]
    return meta, text.lstrip("\n")


def render_toc(entries):
    if not entries:
        return ""
    rows = ['<nav class="toc"><h2 class="toc-h">Table of Contents</h2>']
    for level, text, sid in entries:
        rows.append(
            f'<a class="toc-{level}" href="#{sid}">'
            f'<span class="toc-t">{inline(text)}</span></a>'
        )
    rows.append("</nav>")
    return "".join(rows)


def title_block(meta):
    if not meta.get("title"):
        return ""
    parts = ['<header class="title">']
    if meta.get("eyebrow"):
        parts.append(f'<p class="eyebrow">{inline(meta["eyebrow"])}</p>')
    parts.append(f'<h1 class="doc-t">{inline(meta["title"])}</h1>')
    if meta.get("subtitle"):
        parts.append(f'<p class="doc-s">{inline(meta["subtitle"])}</p>')
    parts.append('<div class="rule"></div>')

    fields = [
        ("Module", "module"), ("Chapter", "chapter"), ("Topic", "topic"),
        ("Version", "version"), ("Compiled", "compiled"), ("Exam stage", "stage"),
    ]
    rows = [
        f'<tr><td class="k">{label}</td><td class="v">{inline(meta[key])}</td></tr>'
        for label, key in fields if meta.get(key)
    ]
    if rows:
        parts.append('<table class="meta">' + "".join(rows) + "</table>")
    parts.append("</header>")
    return "".join(parts)


def build_one(path):
    text = path.read_text(encoding="utf-8")
    meta, body = front_matter(text)

    b = Builder()
    b.run(body.splitlines())
    content = "".join(b.out).replace("\x01TOC\x01", render_toc(b.toc))

    running = meta.get("running", meta.get("title", ""))
    css = CSS.read_text(encoding="utf-8")

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(meta.get('title', path.stem))}</title>
<style>
{css}
</style>
</head>
<body>
<div class="running">{html.escape(running)}
  <span class="ver">{html.escape(meta.get('version', ''))}</span></div>
<main>
{title_block(meta)}
{content}
</main>
<footer class="foot">UPSC EPFO APFC &mdash; Recruitment Test Manual
  &middot; {html.escape(meta.get('chapter', ''))}
  &middot; {html.escape(meta.get('version', ''))}</footer>
</body>
</html>
"""
    rel = path.relative_to(SRC).with_suffix(".html")
    dest = OUT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    return dest, len(b.toc)


def main(argv):
    targets = []
    if len(argv) > 1:
        targets = [Path(a).resolve() for a in argv[1:]]
    else:
        if not SRC.exists():
            print("no src/ directory", file=sys.stderr)
            return 1
        targets = sorted(SRC.rglob("*.md"))

    if not targets:
        print("nothing to build")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    for t in targets:
        dest, headings = build_one(t)
        size = dest.stat().st_size
        print(f"built {dest.relative_to(ROOT)}  ({headings} headings, {size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

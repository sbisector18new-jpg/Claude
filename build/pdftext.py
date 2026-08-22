#!/usr/bin/env python3
"""
pdftext.py - extract text from a PDF using only the standard library.

This sandbox has no pdftotext, pypdf or pymupdf, and no package-manager network
access, so extraction is done here directly.

Scope: PDFs whose text is drawn with simple show operators and whose fonts carry
a /ToUnicode CMap. That covers PDFs produced by a headless-Chrome print pipeline,
which is what the manual's own pdf/ directory contains - so the extractor can be
validated against sources whose exact text is already known.

Usage:  python3 build/pdftext.py FILE.pdf [--check FILE.md]
"""

import re, sys, zlib, os


def objects(data):
    """Map object number -> raw body bytes for every 'N 0 obj ... endobj'."""
    out = {}
    for m in re.finditer(rb'(\d+)\s+\d+\s+obj\b(.*?)\bendobj', data, re.S):
        out[int(m.group(1))] = m.group(2)
    return out


def stream_of(body):
    """Decoded stream bytes of an object body, or None."""
    m = re.search(rb'stream\r?\n?(.*?)\r?\n?endstream', body, re.S)
    if not m:
        return None
    raw = m.group(1)
    if b'/FlateDecode' in body:
        for trim in (0, 1, 2):
            try:
                return zlib.decompress(raw[trim:] if trim else raw)
            except zlib.error:
                continue
        try:
            d = zlib.decompressobj()
            return d.decompress(raw)
        except zlib.error:
            return None
    return raw


def parse_tounicode(cmap):
    """Parse a ToUnicode CMap into {code:int -> str}."""
    table = {}

    def utf16(h):
        b = bytes.fromhex(h)
        try:
            return b.decode('utf-16-be')
        except UnicodeDecodeError:
            return ''

    for blk in re.findall(rb'beginbfchar(.*?)endbfchar', cmap, re.S):
        for src, dst in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            table[int(src, 16)] = utf16(dst.decode())
    for blk in re.findall(rb'beginbfrange(.*?)endbfrange', cmap, re.S):
        for lo, hi, dst in re.findall(
                rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
            a, b = int(lo, 16), int(hi, 16)
            base = int(dst, 16)
            for i in range(a, min(b, a + 65535) + 1):
                try:
                    table[i] = chr(base + (i - a))
                except ValueError:
                    pass
        for m in re.finditer(
                rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]', blk, re.S):
            a = int(m.group(1), 16)
            for k, dst in enumerate(re.findall(rb'<([0-9A-Fa-f]+)>', m.group(3))):
                table[a + k] = utf16(dst.decode())
    return table


def font_maps(objs):
    """
    Build {resource-name -> {code -> str}}.

    Font resource names are matched to font objects through each page's
    /Resources /Font dict, which maps /F3 to an indirect object number.
    """
    tounicode = {}
    for num, body in objs.items():
        if b'/ToUnicode' in body:
            m = re.search(rb'/ToUnicode\s+(\d+)\s+0\s+R', body)
            if m and int(m.group(1)) in objs:
                cm = stream_of(objs[int(m.group(1))])
                if cm:
                    tounicode[num] = parse_tounicode(cm)
    names = {}
    for body in objs.values():
        fm = re.search(rb'/Font\s*<<(.*?)>>', body, re.S)
        if not fm:
            continue
        for name, ref in re.findall(rb'/([A-Za-z0-9+.\-]+)\s+(\d+)\s+0\s+R', fm.group(1)):
            r = int(ref)
            if r in tounicode:
                names.setdefault(name.decode('latin-1'), tounicode[r])
    return names


def unescape(b):
    """Resolve PDF string escapes inside a literal ( ) string."""
    out, i = bytearray(), 0
    while i < len(b):
        c = b[i]
        if c == 0x5C and i + 1 < len(b):
            n = b[i + 1]
            simple = {0x6E: 10, 0x72: 13, 0x74: 9, 0x62: 8, 0x66: 12,
                      0x28: 0x28, 0x29: 0x29, 0x5C: 0x5C}
            if n in simple:
                out.append(simple[n]); i += 2; continue
            m = re.match(rb'[0-7]{1,3}', b[i + 1:i + 4])
            if m:
                out.append(int(m.group(0), 8) & 0xFF); i += 1 + len(m.group(0)); continue
            i += 2; continue
        out.append(c); i += 1
    return bytes(out)


NUM = rb'[-\d.]+'
TOKEN = re.compile(
    rb'/([A-Za-z0-9+.\-]+)\s+[\d.]+\s+Tf'                              # 1 font
    rb'|\((?:\\.|[^\\()])*\)\s*Tj'                                      # literal Tj
    rb'|<[0-9A-Fa-f\s]+>\s*Tj'                                          # hex Tj
    rb'|\[(?:[^\[\]]|\\.)*\]\s*TJ'                                      # array TJ
    rb'|(' + NUM + rb')\s+(' + NUM + rb')\s+Td'                         # 2,3 Td
    rb'|(' + NUM + rb')\s+(' + NUM + rb')\s+TD'                         # 4,5 TD
    rb'|' + NUM + rb'\s+' + NUM + rb'\s+' + NUM + rb'\s+' + NUM +
    rb'\s+(' + NUM + rb')\s+(' + NUM + rb')\s+Tm'                       # 6,7 Tm
    rb'|(T\*)|(BT)|(ET)', re.S)


def decode_show(chunk, table):
    """Decode one show-operator payload to text."""
    text = []
    for m in re.finditer(rb'\((?:\\.|[^\\()])*\)|<([0-9A-Fa-f\s]+)>', chunk, re.S):
        if m.group(1) is not None:
            h = re.sub(rb'\s', b'', m.group(1))
            if len(h) % 2:
                h += b'0'
            codes = [int(h[i:i + 4], 16) for i in range(0, len(h), 4)] \
                if table and max(table) > 255 and len(h) % 4 == 0 \
                else [int(h[i:i + 2], 16) for i in range(0, len(h), 2)]
            text.append(''.join(table.get(c, '') for c in codes) if table
                        else bytes.fromhex(h.decode()).decode('latin-1'))
        else:
            raw = unescape(m.group(0)[1:-1])
            if table:
                # Single-byte codes are the norm for subset TrueType fonts.
                text.append(''.join(table.get(b, chr(b)) for b in raw))
            else:
                text.append(raw.decode('latin-1'))
    return ''.join(text)


def extract(path):
    data = open(path, 'rb').read()
    objs = objects(data)
    fonts = font_maps(objs)
    pages = []
    # Content streams are those decoded streams that contain text operators.
    for num in sorted(objs):
        s = stream_of(objs[num])
        if not s or b'BT' not in s:
            continue
        # Glyph runs are positioned individually by the Chrome pipeline, so a
        # newline cannot be emitted for every positioning operator - that shreds
        # every word. Lines are reconstructed from the y coordinate instead: a
        # new line only when y moves, a space when x jumps forward on the same
        # line, and nothing at all for the many same-position adjustments.
        cur, lines = None, {}
        y = last_x = None
        for m in TOKEN.finditer(s):
            tok = m.group(0)
            if m.group(1):
                cur = fonts.get(m.group(1).decode('latin-1'))
                continue
            gy = m.group(3) or m.group(5) or m.group(7)
            if gy is not None:
                gx = m.group(2) or m.group(4) or m.group(6)
                try:
                    ny, nx = float(gy), float(gx)
                except ValueError:
                    continue
                if tok.endswith(b'TD') or tok.endswith(b'Td'):
                    if y is not None and abs(ny) > 0.01:
                        ny = y + ny
                        nx = last_x + nx if last_x is not None else nx
                    else:
                        ny = y if y is not None else ny
                # No space is synthesised from the x gap. Inter-glyph advances
                # routinely exceed any fixed threshold, which inserted spaces
                # inside words ("E PFO", "recru itm ent") and cost 91 points of
                # word recovery. The embedded strings already carry their spaces.
                y, last_x = ny, nx
                continue
            if tok.endswith(b'Tj') or tok.endswith(b'TJ'):
                txt = decode_show(tok, cur)
                if txt:
                    lines.setdefault(round(y, 1) if y is not None else 0.0,
                                     []).append(txt)
                    last_x = (last_x or 0) + 0.0
        page = '\n'.join(''.join(lines[k]) for k in sorted(lines))
        pages.append(page)
    txt = '\n'.join(pages)
    txt = txt.replace('\u00a0', ' ')
    txt = re.sub(r'[ \t]+', ' ', txt)
    txt = re.sub(r'\n{3,}', '\n\n', txt)
    return txt.strip()


def fidelity(pdf_text, md_path):
    """What fraction of the markdown's words survive into the extracted text?"""
    md = open(md_path, encoding='utf-8').read()
    md = re.sub(r'^---\n.*?\n---\n', '', md, flags=re.S)
    md = re.sub(r'[*`|:#\[\]()>_-]', ' ', md)
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'’]{4,}", md)]
    got = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'’]{4,}", pdf_text))
    if not words:
        return 0.0, 0
    hit = sum(1 for w in words if w.lower() in got)
    return hit / len(words), len(words)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    t = extract(sys.argv[1])
    if '--check' in sys.argv:
        md = sys.argv[sys.argv.index('--check') + 1]
        f, n = fidelity(t, md)
        print('%-46s %5.1f%% of %d words recovered'
              % (os.path.basename(sys.argv[1]), f * 100, n))
    else:
        sys.stdout.write(t)

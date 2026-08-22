#!/usr/bin/env python3
"""
decks.py - build spaced-repetition decks from the APFC manual sources.

Reads src/module-*/*.md and emits Anki-importable TSV files into decks/.

Design principles, in order of importance:

1. RECOGNITION IS NOT RECALL. A multiple-choice item tests recognition: the answer
   is on the page. A flashcard must test free recall. Every card here therefore
   either deletes the fact from its own sentence (cloze) or asks a question whose
   answer is not visible. MCQ options are never reproduced on a card front.

2. ONE FACT PER CARD. Wall-sheet lines carrying several facts separated by the
   middot are split. A card that holds two facts fails for the wrong reason and
   teaches nothing about which half was forgotten.

3. DISCRIMINATION BEATS ASSERTION. The manual's own thesis (F11.4) is that the
   paper is lost to confusion between neighbouring facts, not to ignorance. So the
   confusion tables become their own deck, and those cards name the distractor
   explicitly. Knowing 15,000 is worth little if 6,500 feels equally familiar.

4. NUMBERS DECAY FASTEST. Figures, dates and section numbers get their own deck so
   they can be reviewed on a shorter interval than prose.

5. NEVER FABRICATE A QUESTION. Where a statement has no clozeable target and no
   natural split, it is skipped and counted, not turned into a vague prompt.
"""

import re, os, glob, sys, unicodedata
from collections import defaultdict, Counter

SRC = 'src'
OUT = 'decks'
INCOMING = 'incoming'

# ---------------------------------------------------------------- text handling

def md_to_html(s):
    """Markdown inline -> minimal HTML. Anki is imported with #html:true."""
    s = s.replace('\\', '')
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def plain(s):
    """Strip all markup and HTML, for dedupe keys and for measuring."""
    s = re.sub(r'<[^>]+>', '', md_to_html(s))
    # Currency stamps such as "[AS AT 16 AUG 2026]" date the page, not the fact.
    # Left in, the date becomes the most tempting cloze target on the card.
    s = re.sub(r'\[\s*AS AT[^\]]*\]', '', s, flags=re.I)
    # Answer-key restatements leak from explanation text: "1 and 2 only.", "(c)".
    s = re.sub(r'^\(?[a-d]\)\s+', '', s)
    s = re.sub(r'^(?:only\s+)?[\d, and]+only\.\s*', '', s, flags=re.I)
    s = re.sub(r'^(?:Statements?\s+)?[IVX\d, and]+\s+(?:only|are correct)\.\s*', '',
               s, flags=re.I)
    return re.sub(r'\s+', ' ', s).strip()

def key(s):
    """Normalised dedupe key."""
    s = plain(s).lower()
    s = unicodedata.normalize('NFKD', s)
    return re.sub(r'[^a-z0-9]+', '', s)

def tsv(s):
    """Make a string safe for one TSV field."""
    return plain_html(s).replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')

def plain_html(s):
    return re.sub(r'\s+', ' ', s).strip()

# ------------------------------------------------------------- figure detection

MONTHS = (r'January|February|March|April|May|June|July|August|September|October|'
          r'November|December')

FIGURE_PATTERNS = [
    # Ranges and ratios are single atomic facts. Clozing half of "1.5-3.5" or of
    # "0.5:1" produces a card that cannot be answered, so they must match first
    # and as a whole.
    r'₹\s?[\d,]+(?:\.\d+)?\s*[–—-]\s*₹?\s?[\d,]+(?:\.\d+)?',
    # A fiscal or academic year is one token: "2022-23", "2025-26".
    r'\b(?:1[6-9]|20)\d{2}\s*[–—-]\s*\d{2}\b',
    r'\b\d+(?:\.\d+)?\s*[–—]\s*\d+(?:\.\d+)?\b',
    r'\b\d+(?:\.\d+)?\s*:\s*\d+(?:\.\d+)?\b',
    r'₹\s?[\d,]+(?:\.\d+)?(?:\s*(?:lakh|crore|thousand))?',
    r'\d+(?:\.\d+)?\s*(?:%|per cent)',
    r'\b\d{1,2}\s+(?:' + MONTHS + r')\s+\d{4}\b',
    r'\b(?:' + MONTHS + r')\s+\d{4}\b',
    r'\b(?:1[6-9]|20)\d{2}\b',
    r'\b\d+(?:\.\d+)?\s*(?:days?|weeks?|months?|years?|hours?|minutes?|marks?|'
    r'members?|workers?|persons?|employees?|questions?|lakh|crore|times?|'
    r'bits?|bytes?|km|kg|litres?|degrees?)\b',
    r'\b(?:[Ss]ection|[Aa]rticle|[Ee]ntry|[Cc]onvention|[Cc]hapter)\s+\d+[A-Z]*\b',
    r'\b(?:[Ff]irst|[Ss]econd|[Tt]hird|[Ff]ourth|[Ff]ifth|[Ss]ixth|[Ss]eventh|'
    r'[Ee]ighth|[Nn]inth|[Tt]enth|[Ee]leventh|[Tw]elfth)\s+[Ss]chedule\b',
    r'\b\d+(?:st|nd|rd|th)\s+[Aa]mendment\b',
    # Generic numerals, but two digits or more. A bare single digit is almost
    # always structural rather than factual - the 1 in "1/v + 1/u = 1/f", the 3
    # in "1/3" - and clozing it teaches nothing. Single digits that do carry a
    # fact are caught above by their unit or currency.
    r'(?<![\w./])\d{2,}(?:,\d{3})*(?:\.\d+)?(?![\w.%/])',
]

# Blocks that are instructions to the reader, not facts about the world.
PROCEDURAL = re.compile(
    r"tonight's drill|per F\d+\.\d|timed at|this cell|week \d+ \w+ cell|"
    r'mark it in the booklet|write it in your own words|log it|do this now'
    # Self-referential prose. "F3.1's finding, now the subject of this chapter"
    # is a sentence about the manual, not a fact about the world.
    r"|this chapter|this section|the subject of this|F\d+\.\d+'s finding",
    re.I)

# Running heads, footers and page furniture. Harmless in markdown, where they do
# not exist, but a PDF puts them on every page and they mine as facts:
# "Chapter F1.13 Page 25" became a card.
FURNITURE = re.compile(
    r'^\s*(?:UPSC\s+EPFO|Foundation\s+F\d|APFC\s+FOUNDATION|Table of Contents)'
    r'|Page\s+\d+\s*$|^\s*Chapter\s+F?\d+\.\d+\s*(?:Page\s*\d+)?\s*$'
    r'|^\s*\d+\s*$', re.I)


def welded(ptxt):
    """
    True when a line is several separate facts run together.

    A PDF has no paragraph structure, so wall-sheet entries that were visually
    distinct arrive on one line. Clozing such a line produces a card holding
    three facts, which fails for the wrong reason and teaches nothing. Two
    signals catch it: length, and a run of several distinct capitalised labels.
    """
    if len(ptxt) > 150:
        return True
    if len(re.findall(r'\b[A-Z][A-Z&\'-]{5,}\b', ptxt)) > 2:
        return True
    # "Liberal 44, 45, 48, 48A, 49" - clozing one item of an enumeration.
    if len(re.findall(r'\d+[A-Z]?\s*,', ptxt)) >= 3:
        return True
    return False
FIG_RE = re.compile('|'.join('(?:%s)' % p for p in FIGURE_PATTERNS))

# Figures too generic to be worth deleting on their own.
FIG_STOP = {'one', 'two', 'i', 'ii', 'iii', 'iv', 'v'}

def figures(text):
    """Distinct figure spans in text, longest-first, non-overlapping."""
    spans = []
    for m in FIG_RE.finditer(text):
        s, e = m.span()
        if any(not (e <= a or s >= b) for a, b in spans):
            continue
        tok = m.group(0).strip()
        if tok.lower() in FIG_STOP or len(tok) == 0:
            continue
        spans.append((s, e))
    return sorted(spans)

# ------------------------------------------------------------------ card holder

class Deck:
    def __init__(self, name, notetype, deckname, fields):
        self.name, self.notetype, self.deckname, self.fields = name, notetype, deckname, fields
        self.rows, self.seen = [], set()

    def add(self, front, back, tags, dedupe=None):
        k = key(dedupe if dedupe is not None else front)
        if not k or k in self.seen:
            return False
        self.seen.add(k)
        self.rows.append((tsv(front), tsv(back), ' '.join(tags)))
        return True

    def write(self, outdir):
        path = os.path.join(outdir, self.name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write('#separator:tab\n#html:true\n')
            f.write('#notetype:%s\n' % self.notetype)
            f.write('#deck:%s\n' % self.deckname)
            f.write('#tags column:3\n')
            for r in self.rows:
                f.write('\t'.join(r) + '\n')
        return path, len(self.rows)

# ------------------------------------------------------------------ front matter

def front_matter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    d = {}
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                d[k.strip()] = v.strip()
    return d

SYLLABUS = {
    '01': 'polity', '02': 'labour-law', '03': 'social-security', '04': 'economy',
    '05': 'accounting', '06': 'accounting', '07': 'insurance', '08': 'english-quant',
    '09': 'science', '10': 'current-affairs', '11': 'exam-craft', '12': 'interview',
}

def blocks(section_text):
    """Split a section body into logical blocks, joining wrapped lines."""
    out, cur = [], []
    for line in section_text.split('\n'):
        st = line.strip()
        if not st:
            if cur:
                out.append(' '.join(cur)); cur = []
            continue
        if st.startswith(':::') or st.startswith('#') or st.startswith('^'):
            if cur:
                out.append(' '.join(cur)); cur = []
            continue
        if st.startswith('|'):
            if cur:
                out.append(' '.join(cur)); cur = []
            continue
        cur.append(st)
    if cur:
        out.append(' '.join(cur))
    return out

def tidy_part(p):
    """Strip stray/unbalanced emphasis markers left by splitting."""
    p = p.strip().strip('·').strip()
    if p.count('**') % 2:
        p = p.replace('**', '')
    return p.strip(' —-·,;')


def split_middot(block):
    """
    Split a wall-sheet block into single facts, preserving the label as context.

    A wall-sheet block is written as  **LABEL** fact · fact · fact  and may wrap
    across physical lines. Splitting naively on the middot throws the label away
    and leaves fragments like "path feeling" that mean nothing on a card front.
    So the label is extracted first and re-attached to every fact taken from the
    block, which is both correct and makes a far better card.
    """
    b = block.strip()
    label = ''
    m = re.match(r'^\*\*([^*]{3,60})\*\*\s*(.*)$', b, re.S)
    if m and not m.group(2).strip().startswith('·'):
        label, rest = m.group(1).strip(), m.group(2).strip()
        if not rest:
            label, rest = '', b
    else:
        rest = b

    parts = [tidy_part(p) for p in re.split(r'\s*·\s*', rest)]
    parts = [p for p in parts if len(plain(p)) >= 10 and len(plain(p).split()) >= 2]
    if not parts:
        parts = [tidy_part(rest)] if len(plain(rest)) >= 10 else []

    out = []
    for p in parts:
        pk, lk = key(p), key(label)
        if label and lk and lk not in pk and len(plain(p)) < 200:
            out.append('%s — %s' % (label, p))
        else:
            out.append(p)
    return out


# Ordered cloze strategies for a statement with no figure in it.
SEP_RULES = [
    r'^(?P<a>.{6,}?)\s+(?:=|»|→|>)\s+(?P<b>.{3,})$',
    r'^(?P<a>[^:]{6,}?):\s+(?P<b>.{4,})$',
    r'^(?P<a>.{10,}?)\s+—\s+(?P<b>.{6,})$',
    r'^(?P<a>.{6,}?),\s+(?:NOT|not)\s+(?P<b>.{3,})$',
    r'^(?P<a>.{8,}?)\s+(?:is|are|means|becomes|equals)\s+(?P<b>.{4,})$',
    r'^(?P<a>.{10,}?),\s+(?P<b>.{10,})$',
]


def cloze_no_figure(ptxt):
    """Return cloze text for a figure-free statement, or None."""
    for rx in SEP_RULES:
        m = re.match(rx, ptxt)
        if m and len(plain(m.group('b'))) >= 4:
            sep = ptxt[m.end('a'):m.start('b')]
            return '%s%s{{c1::%s}}' % (m.group('a'), sep, m.group('b'))
    # Wall-sheet shorthand: an upper-case slogan with no separator at all.
    words = ptxt.split()
    letters = re.sub(r'[^A-Za-z]', '', ptxt)
    if len(words) >= 4 and letters and sum(c.isupper() for c in letters) / len(letters) > 0.8:
        n = 2 if len(words) >= 6 else 1
        return '%s {{c1::%s}}' % (' '.join(words[:-n]), ' '.join(words[-n:]))
    return None


# ------------------------------------------------------- discrimination tables
#
# Matched by exact header signature rather than by keyword, because keyword
# matching swept in every answer-explanation table whose header happens to carry
# the word "Trap" and produced 264 cards reading "Front: 5 / Back: c". A
# whitelist is auditable: every entry below was read before being added.
#
#   key   = tuple of header cells, lower-cased
#   value = (index of item, index of correct, index of wrong or None, reversed)

DISC_TABLES = {
    ('item', 'current value', 'the confusable value'): (0, 1, 2),
    ('subject', 'live instrument', 'now superseded — and therefore a distractor'): (0, 1, 2),
    ('rule', 'right', 'wrong'): (0, 1, 2),
    ('wrong', 'right'): (None, 1, 0),
    ('the old answer', 'the current answer'): (None, 1, 0),
    ('do', 'do not'): (None, 0, 1),
    ('material but not pervasive', 'material and pervasive'): (None, 0, 1),
}

# Two-column tables whose right cell is itself the discriminating statement.
DISC_LINE_TABLES = {
    ('pair', 'the discriminating line'),
    ('comparison', 'the discriminating line'),
}

# Definition and matching tables: good basic cards, term -> meaning.
DEF_TABLES = {
    ('term', 'meaning'), ('word', 'meaning'), ('term', 'what it is'),
    ('type', 'meaning'), ('section', 'content'), ('list-i', 'list-ii'),
    ('item', 'reading'), ('idea', 'statement'), ('result', 'statement'),
}

# ------------------------------------------------------------------------ build

def main():
    d_num = Deck('apfc-1-numbers.tsv', 'Cloze', 'APFC::1 Numbers and Dates',
                 ['Text', 'Back Extra'])
    d_disc = Deck('apfc-2-discrimination.tsv', 'Basic', 'APFC::2 Discrimination',
                  ['Front', 'Back'])
    d_fact = Deck('apfc-3-core-facts.tsv', 'Cloze', 'APFC::3 Core Facts',
                  ['Text', 'Back Extra'])
    d_qrec = Deck('apfc-4-question-recall.tsv', 'Basic', 'APFC::4 Question Recall',
                  ['Front', 'Back'])
    d_def = Deck('apfc-5-definitions.tsv', 'Basic', 'APFC::5 Definitions and Pairs',
                 ['Front', 'Back'])
    d_trap = Deck('apfc-6-traps.tsv', 'Basic', 'APFC::6 Traps', ['Front', 'Back'])
    d_ivw = Deck('apfc-7-interview.tsv', 'Basic', 'APFC::7 Interview', ['Front', 'Back'])

    stats = Counter()
    skipped = []

    sources = load_sources()
    if not sources:
        sys.exit('no sources found under %s or %s' % (SRC, INCOMING))

    for path, text, modnum, ch, strict in sources:
        fm = front_matter(text)
        ch = ch or fm.get('chapter', '').replace('Chapter ', '').strip()
        base_tags = ['APFC::M%s::%s' % (modnum, ch.replace('.', '_')),
                     'syllabus::%s' % SYLLABUS.get(modnum, 'other')]

        # ---- 1. wall sheets and one-minute revision -> numbers + core facts
        for m in re.finditer(
                r'^## \d+\.\s*(?:Five-Minute Wall Sheet|One-Minute Revision)[^\n]*\n(.*?)(?=^## |\Z)',
                text, re.S | re.M):
            for blk in blocks(m.group(1)):
                if 'ONE LINE FOR THE INTERVIEW' in blk:
                    line = re.sub(r'^\**ONE LINE FOR THE INTERVIEW\**\s*', '', blk).strip()
                    if len(plain(line)) > 40:
                        d_ivw.add('Speak for thirty seconds: %s<br><br><i>(%s)</i>'
                                  % (topic_of(fm), ch),
                                  md_to_html(line),
                                  base_tags + ['type::interview'],
                                  dedupe=line)
                        stats['interview'] += 1
                    continue
                if PROCEDURAL.search(plain(blk)):
                    stats['skipped-procedural'] += 1
                    continue
                for fact in split_middot(blk):
                    ptxt = plain(fact)
                    if len(ptxt) < 12 or len(ptxt) > 320:
                        continue
                    if FURNITURE.search(ptxt):
                        stats['skipped-page-furniture'] += 1
                        continue
                    if strict and welded(ptxt):
                        stats['skipped-welded-pdf-line'] += 1
                        continue
                    figs = figures(ptxt)
                    if figs:
                        made = 0
                        for (s, e) in figs[:2]:
                            cl = ptxt[:s] + '{{c1::' + ptxt[s:e] + '}}' + ptxt[e:]
                            if d_num.add(cl, ch, base_tags + ['type::numbers'],
                                         dedupe=cl):
                                stats['numbers'] += 1
                                made += 1
                        if made:
                            continue
                    cl = cloze_no_figure(ptxt)
                    if cl:
                        if d_fact.add(cl, ch, base_tags + ['type::fact'], dedupe=cl):
                            stats['facts'] += 1
                        continue
                    skipped.append((ch, ptxt[:90]))
                    stats['skipped-no-target'] += 1

        # ---- 2. whitelisted tables -> discrimination and definition decks
        for m in re.finditer(r'^\|(.+)\|[ \t]*\n\|[-: |]+\|[ \t]*\n((?:\|.*\n)+)',
                             text, re.M):
            hdr = tuple(re.sub(r'[*`]', '', h.strip()).lower()
                        for h in m.group(1).split('|') if h.strip())
            rows = [[c.strip() for c in r.strip().strip('|').split('|')]
                    for r in m.group(2).strip().split('\n')]

            if hdr in DISC_TABLES:
                i_item, i_ok, i_bad = DISC_TABLES[hdr]
                for cells in rows:
                    if len(cells) < len(hdr):
                        continue
                    ok = cells[i_ok]
                    bad = cells[i_bad] if i_bad is not None else ''
                    item = cells[i_item] if i_item is not None else ''
                    if not plain(ok):
                        continue
                    if item:
                        front = ('<b>%s</b><br><br>The correct fact — and the '
                                 'distractor you must refuse?' % md_to_html(item))
                        back = '&#10003; %s' % md_to_html(ok)
                        if plain(bad) and plain(bad) != '—':
                            back += '<br><br>&#10007; <i>Not</i> %s' % md_to_html(bad)
                        dk = item + '|' + ok
                    else:
                        front = ('Right or wrong, and why?<br><br>%s'
                                 % md_to_html(bad or ok))
                        back = '&#10007; Wrong.<br><br>&#10003; %s' % md_to_html(ok)
                        dk = (bad or ok) + '|' + ok
                    if d_disc.add(front, back, base_tags + ['type::discrimination'],
                                  dedupe=dk):
                        stats['discrimination'] += 1

            elif hdr in DISC_LINE_TABLES:
                for cells in rows:
                    if len(cells) < 2 or not plain(cells[1]):
                        continue
                    front = ('Give the discriminating line.<br><br><b>%s</b>'
                             % md_to_html(cells[0]))
                    if d_disc.add(front, md_to_html(cells[1]),
                                  base_tags + ['type::discrimination'],
                                  dedupe='pair|' + cells[0]):
                        stats['discrimination'] += 1

            elif hdr in DEF_TABLES:
                for cells in rows:
                    if len(cells) < 2:
                        continue
                    a, b = plain(cells[0]), plain(cells[1])
                    if len(a) < 3 or len(b) < 6 or len(a) > 120:
                        continue
                    if d_def.add(md_to_html(cells[0]), md_to_html(cells[1]),
                                 base_tags + ['type::definition'],
                                 dedupe=a + '|' + b):
                        stats['definitions'] += 1

        # ---- 3. MCQ stems + answer tables -> free-recall deck
        qtext = {}
        for m in re.finditer(r'^\*\*Q(\d+)\.\*\*\s*(.*?)(?=^\*\*Q\d+\.\*\*|^#|^:::|\Z)',
                             text, re.S | re.M):
            qtext[m.group(1)] = m.group(2)
        for m in re.finditer(r'^\|\s*(\d+)\s*\|\s*([a-d])\s*\|(.+?)\|\s*$', text, re.M):
            qno, ans, rest = m.group(1), m.group(2), m.group(3)
            cells = [c.strip() for c in rest.split('|')]
            expl = cells[-1]
            if len(plain(expl)) < 25:
                continue
            stem_raw = qtext.get(qno, '')
            stem = strip_options(stem_raw)
            pstem = plain(stem)
            if stem_ok(pstem):
                front = md_to_html(stem)
                back = md_to_html(expl)
                if d_qrec.add(front, back, base_tags + ['type::recall'],
                              dedupe=front):
                    stats['question-recall'] += 1
            else:
                # stem needs its options to make sense: cloze the explanation instead
                pex = plain(expl)
                figs = figures(pex)
                if figs and 30 <= len(pex) <= 300:
                    s, e = figs[0]
                    cl = pex[:s] + '{{c1::' + pex[s:e] + '}}' + pex[e:]
                    if d_num.add(cl, ch, base_tags + ['type::numbers'], dedupe=cl):
                        stats['numbers-from-explanations'] += 1
                else:
                    stats['skipped-stem-needs-options'] += 1

    # ---- 4. traps
    tf = os.path.join(SRC, 'module-11', 'F11.4-trap-catalogue.md')
    if os.path.exists(tf):
        t = open(tf, encoding='utf-8').read()
        for m in re.finditer(r'^#### (T-\d+)\s+(.+?)\s*(★+☆*)?\s*\n(.*?)(?=^#### |^### |^## |\Z)',
                             t, re.S | re.M):
            code, name, stars, body = m.group(1), m.group(2), m.group(3) or '', m.group(4)
            shape = field(body, 'Shape')
            remedy = field(body, 'Remedy')
            if not remedy:
                # A trap without a stated remedy is a defect in the chapter, not a
                # card to be quietly dropped. Fail loudly so it gets fixed.
                sys.stderr.write('WARNING: %s has no **Remedy.** in F11.4\n' % code)
                stats['trap-missing-remedy'] += 1
                continue
            front = '<b>%s %s</b> %s<br><br>%s<br><br>What is the remedy?' % (
                code, md_to_html(name), stars, md_to_html(shape) if shape else '')
            d_trap.add(front, md_to_html(remedy),
                       ['APFC::M11::F11_4', 'syllabus::exam-craft', 'type::trap', code],
                       dedupe=code)
            stats['traps'] += 1

    os.makedirs(OUT, exist_ok=True)
    total = 0
    print('%-34s %6s' % ('deck', 'cards'))
    print('-' * 42)
    for d in (d_num, d_disc, d_fact, d_qrec, d_def, d_trap, d_ivw):
        p, n = d.write(OUT)
        total += n
        print('%-34s %6d' % (os.path.basename(p), n))
    print('-' * 42)
    print('%-34s %6d' % ('TOTAL', total))
    print()
    for k, v in sorted(stats.items()):
        print('  %-32s %5d' % (k, v))
    with open(os.path.join(OUT, '.skipped.txt'), 'w', encoding='utf-8') as f:
        for ch, s in skipped:
            f.write('%s\t%s\n' % (ch, s))
    return total


def pdf_to_markdownish(text):
    """
    Reshape extracted PDF text so the markdown miners can read it.

    A PDF has thrown away the distinctions the miners rely on: which lines are
    wall-sheet facts, which tables are confusion tables, where bold began. What
    survives reliably is the section headings and the line breaks, so those are
    rebuilt and each visual line is made its own block. Continuation lines are
    rejoined when the previous line clearly did not end.
    """
    lines = [l.rstrip() for l in text.split('\n')]
    out, buf = [], ''
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if re.match(r'^\d+\.\s+[A-Z]', s):
            if buf:
                out.append(buf); buf = ''
            out.append('## ' + s); continue
        if re.match(r'^\d+\.\d+\s+\S', s):
            if buf:
                out.append(buf); buf = ''
            out.append('### ' + s); continue
        # A line that ends mid-clause continues into the next one.
        if buf and not re.search(r'[.!?:;·]$', buf) and s[:1].islower():
            buf += ' ' + s
        else:
            if buf:
                out.append(buf)
            buf = s
    if buf:
        out.append(buf)
    return '\n\n'.join(out)


def select_incoming():
    """
    Choose one file per chapter from incoming/, and say what was dropped.

    An upload arrives as people actually have it: browser duplicates ending
    " (1)", two editions of the same module under different naming schemes, and
    compilation volumes covering a chapter range. Taking all of them would double
    some chapters and mis-file others, so selection is explicit and logged rather
    than left to whichever file the glob happened to reach first.
    """
    cands = {}
    dropped = []
    for path in sorted(glob.glob(os.path.join(INCOMING, '**', '*'), recursive=True)):
        base = os.path.basename(path)
        if not path.lower().endswith(('.md', '.pdf')) or base.lower() == 'readme.md':
            continue
        if re.search(r'\s\(\d+\)\.(pdf|md)$', base, re.I):
            dropped.append((base, 'duplicate download'))
            continue
        if re.search(r'\bChapters?\s+\d+\.\d+\s+to\s+\d+\.\d+', base, re.I):
            dropped.append((base, 'compilation volume, superseded by single chapters'))
            continue
        m = re.search(r'\bF?(\d{1,2})\.(\d{1,2})\b', base)
        if not m:
            dropped.append((base, 'no chapter code in filename'))
            continue
        code = 'F%s.%s' % (m.group(1), m.group(2))
        # Preference: the FOUNDATION edition, then the larger file. On this
        # upload the FOUNDATION files are both fuller and more current - they
        # carry the 21 November 2025 commencement, the older edition does not.
        rank = (1 if re.search(r'FOUNDATION', base, re.I) else 0, os.path.getsize(path))
        if code not in cands or rank > cands[code][0]:
            if code in cands:
                dropped.append((os.path.basename(cands[code][1]),
                                'superseded by a better copy of %s' % code))
            cands[code] = (rank, path)
        else:
            dropped.append((base, 'superseded by a better copy of %s' % code))

    if dropped:
        sys.stderr.write('incoming/: %d file(s) not used\n' % len(dropped))
        for b, why in sorted(dropped):
            sys.stderr.write('   %-62s %s\n' % (b[:62], why))
    return [p for _, p in sorted(cands.values(), key=lambda t: t[1])]


def load_sources():
    """
    Yield (path, markdown-ish text, module number, chapter code).

    Markdown under src/ is used as-is. Anything dropped into incoming/ is picked
    up too, so the missing modules can be added without touching this file:
    .md goes straight through, .pdf is extracted first.
    """
    out = []
    for path in sorted(glob.glob(os.path.join(SRC, 'module-*', '*.md'))):
        text = open(path, encoding='utf-8').read()
        mod = re.search(r'module-(\d+)', path).group(1)
        fm = front_matter(text)
        ch = fm.get('chapter', '').replace('Chapter ', '').strip() or \
            os.path.basename(path)
        out.append((path, text, mod, ch, False))

    for path in select_incoming():
        low = path.lower()
        m = re.search(r'\bF?(\d{1,2})\.(\d{1,2})\b', os.path.basename(path))
        mod, ch = m.group(1).zfill(2), 'F%s.%s' % (m.group(1), m.group(2))
        if low.endswith('.md'):
            out.append((path, open(path, encoding='utf-8').read(), mod, ch, False))
        elif low.endswith('.pdf'):
            try:
                sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
                import pdftext
                raw = pdftext.extract(path)
            except Exception as e:                       # noqa: BLE001
                sys.stderr.write('WARNING: could not read %s (%s)\n' % (path, e))
                continue
            out.append((path, pdf_to_markdownish(raw), mod, ch, True))
    return out


def topic_of(fm):
    t = fm.get('title', '')
    return t.split('—')[0].strip() if '—' in t else t


def field(body, name):
    m = re.search(r'\*\*%s\.\*\*\s*(.+?)(?=\n\n\*\*|\Z)' % name, body, re.S)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def strip_options(stem):
    """Remove the (a)...(d) option run from a question stem."""
    i = stem.find('(a)')
    if i == -1:
        i = stem.find('(a')
    return (stem[:i] if i > 0 else stem).strip()


BAD_STEM = re.compile(
    r'which of the following|of the above|consider the following|given below|'
    r'match|arrange|chronolog|assertion|reason \(r\)|statement i+\b|'
    r'how many|correctly matched|not correct|is incorrect|except\b|'
    r'select the|choose the|following pairs|following statements',
    re.I)


def stem_ok(pstem):
    """True when the stem is answerable without its options."""
    if not (25 <= len(pstem) <= 260):
        return False
    if BAD_STEM.search(pstem):
        return False
    if pstem.count('(') > 1:
        return False
    return True


if __name__ == '__main__':
    main()

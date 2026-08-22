# decks — spaced repetition for the APFC manual

**7,068 cards, generated from the manual's own sources — all twelve modules.** Rebuild at any time with:

```
python3 build/decks.py
```

The files are Anki-importable TSV. They carry header directives, so import is one
click with no column mapping: **File → Import**, choose the file, **Import**. The
note type, destination deck and tag column are all declared inside each file.

| File | Note type | Cards | What it is for |
|---|---|---:|---|
| `apfc-1-numbers.tsv` | Cloze | 2,994 | Every figure, date, section and threshold. Reviewed on the shortest interval, because numbers decay fastest and the paper attacks them hardest |
| `apfc-2-discrimination.tsv` | Basic | 131 | Neighbouring facts, with the distractor named. The most valuable deck per card |
| `apfc-3-core-facts.tsv` | Cloze | 2,611 | The wall sheets, one fact to a card |
| `apfc-4-question-recall.tsv` | Basic | 967 | Practice items turned from recognition into free recall |
| `apfc-5-definitions.tsv` | Basic | 293 | Term-to-meaning and List-I/List-II pairs |
| `apfc-6-traps.tsv` | Basic | 30 | T-01 to T-30 of F11.4 — shape on the front, remedy on the back |
| `apfc-7-interview.tsv` | Basic | 42 | The one-line interview answers, prompted as *speak for thirty seconds* |

Tags are hierarchical, so any slice can be studied on its own:
`APFC::M09::F9_3`, `syllabus::labour-law`, `type::numbers`.

## The four rules these cards were built on

**1. Recognition is not recall.** A multiple-choice item tests recognition — the
answer is on the page. Options are therefore never reproduced on a card front.
Every card either deletes the fact from its own sentence or asks a question whose
answer is not visible.

**2. One fact to a card.** Wall-sheet lines carrying several facts are split. A
card holding two facts fails for the wrong reason, and tells you nothing about
which half you had forgotten.

**3. Discrimination beats assertion.** F11.4's thesis is that this paper is lost to
confusion between adjacent facts, not to ignorance. Knowing that the ceiling is
₹15,000 is worth little while ₹6,500 feels equally familiar, so those cards name
the distractor and ask you to refuse it.

**4. Never fabricate a question.** Where a statement had no clozeable target and no
natural split, it was skipped and counted rather than turned into a vague prompt.
3,268 lines were dropped that way — including 897 welded PDF lines and 393 page
headers — and every count is printed on each build.

## The PDF modules

Modules **1, 2, 3 and 5** — 97.5 of the 300 planning marks — are read from
`incoming/` as **PDFs**, and contribute **2,643 cards: facts and figures only.**
They produce **no** discrimination cards and **no** question-recall cards, because
those need the confusion tables and answer grids to survive as tables, and a PDF
has flattened them. F11.7 §2.2 has the split. **If markdown exists for those four
modules, supply it** — one rebuild converts them to full sources.

## Schedule

Cards without a schedule are a filing cabinet. **F11.7** is the protocol: which
deck at which interval, what to do on a lapse, and how the decks interact with the
mocks and the error log. Read it before importing anything.

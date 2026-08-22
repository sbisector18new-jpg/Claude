# incoming — the Module 1, 2, 3 and 5 sources

**Received: 44 chapters as PDFs**, covering Modules 1, 2, 3 and 5 — **97.5 of the
300 planning marks.** These are live sources: `build/decks.py` reads them on every
run, and they contribute **2,643 of the 7,068 cards** in `decks/`.

Six of the 50 uploaded files are not used, and the build prints why on every run:

| Not used | Reason |
|---|---|
| 2 files ending ` (1).pdf` | Duplicate downloads |
| 3 files named `APFC Module 1 - Chapter 1.x` | Superseded by the `FOUNDATION - Chapter F1.x` edition, which is fuller (13,316 words against 6,081 for chapter 1.1) and current, citing the **21 November 2025** commencement that the older edition does not mention |
| `Chapters 1.4 to 1.13 - Completion Volume` | Compilation, superseded by the individual FOUNDATION chapters |

## Markdown would still be a real upgrade

These 44 chapters yield **facts and figures only** — no discrimination cards, no
question-recall cards. Both need structure a PDF has thrown away: a confusion
table must still be a **table**, and question recall needs the
`| Q | Ans | Explanation |` grid. F11.7 §2.2 has the numbers.

So **if the markdown sources exist anywhere, add them** and delete the matching
PDFs. One rebuild converts these four modules from partial sources to full ones.
Measured on one chapter built both ways: markdown 97 cards, its PDF 71.

## How to upload more


Open this link, drag **all** the files in at once, scroll down, and commit:

<https://github.com/sbisector18new-jpg/Claude/upload/decks/retention-engine/incoming>

There is no file-count limit on that page, so all 39 go in one action. GitHub's
web upload caps individual files at 25 MB, which these are comfortably under.

## Markdown is much better than PDF, if you have it

| You upload | What happens | Cards recovered |
|---|---|---|
| `.md` sources | Dropped into `src/module-0N/`, decks rebuild exactly as for the other eight modules | 100% |
| `.pdf` only | Text is extracted by `build/pdftext.py`, then mined | **73%** |

Both figures are measured, not estimated. Extraction recovers **95.6%** of words,
checked across all 43 PDFs already in this repo against their known sources. Then
the same chapter was built both ways: markdown gave 97 cards, PDF gave 71.

The gap is not the text. It is **structure**. The deck builder reads meaning from
markdown that a PDF has thrown away — which lines are wall-sheet facts, which
tables are confusion tables, where a question ends and its explanation begins.
Nearly the whole of the missing quarter is the **question-recall** deck, which
needs the `| Q | Ans | Explanation |` tables to survive as tables.

So: upload `.md` if it exists anywhere. Upload the PDFs if it does not. Both work.

## Naming

Keep whatever names you have — the loader reads the chapter code out of the
filename, so `APFC FOUNDATION - Chapter F1.1 - Constitutional Foundations from
Zero - v1.0.pdf` is fine and routes itself to Module 1.

Once the files are here, say so, and the decks are rebuilt across all twelve
modules in one pass.

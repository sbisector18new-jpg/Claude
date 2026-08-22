# incoming — drop the missing-module files here

Modules 1, 2, 3 and 5 are listed in the Master Content Register but their sources
are not in `src/`. That is 44 chapters and **97.5 of the 300 planning marks**, and
it is why the decks in `decks/` currently cover eight modules rather than twelve.

## How to upload

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

# UPSC EPFO APFC — Recruitment Test Manual

A self-study manual for the UPSC EPFO **Assistant Provident Fund Commissioner (APFC) Recruitment
Test (RT)**. Built for roughly 2 hours of study a day, optimised for marks per hour rather than
coverage.

> The written stage is called the **Recruitment Test**, never "Prelims" — there is no Mains. It
> carries **75%** of the final merit (300 of 400 marks), and its marks are *not* discarded, so every
> extra RT mark is a permanent gain.

## Start here

| | |
|---|---|
| **Project state** | [`MASTER_CONTENT_REGISTER.md`](MASTER_CONTENT_REGISTER.md) — what is complete, what remains, study order, schedule |
| **Built chapters** | [`docs/index.html`](docs/index.html) — open in a browser, then print to PDF |
| **Manuscript** | [`src/`](src/) — Markdown sources, the source of truth |

## Where the project stands

- **Complete:** Modules 1, 2, 3, 5 — 44 chapters, 100 hours, 109.5 planning marks
- **Remaining:** Modules 4, 6, 7, 8, 9, 10, 11 — 124 hours, 190.5 planning marks
- **In progress:** Module 6 — Accounting, Auditing and Statistics (F6.1 complete)

## The two layers

Chapters come in two forms, and using the wrong one at the wrong time wastes study time.

| Layer | Prefix | What it does | When to use it |
|---|---|---|---|
| **Foundation** | `F6.1` | Teaches from zero. Defines every term on first use, explains *why* a rule exists before stating it, worked examples, graded practice | Your first pass through a subject you do not already know |
| **Compact** | `6.1` | Dense, evidence-led, built around what the paper has actually asked. Numbers tables, one-minute revisions, wall sheets | Final six weeks, and every revision pass after the first |

Foundation first to understand, Compact second to compress — never the other way round. A compressed
note is only compressible because it assumes a foundation.

## Building

```sh
python3 build/build.py                                          # everything
python3 build/build.py src/module-06/F6.1-accounting-fundamentals.md   # one file
```

Python 3 stdlib only, no third-party packages. `docs/` is generated output — never edit it by hand.

**To get a PDF:** open a built HTML file and print to PDF from the browser (Ctrl/Cmd-P → Save as
PDF). This sandbox has no PDF toolchain and cannot reach PyPI, so browser printing is the delivery
route; the stylesheet is built for A4 and keeps callouts, tables and question blocks from splitting
across pages.

## Evidence labels

Every factual claim carries a label, because confidently stated APFC "weightage" figures are usually
invented.

| Label | Meaning |
|---|---|
| **OFFICIAL** | Stated by UPSC or a Government of India source |
| **PYQ-DERIVED** | Counted from an actual question paper |
| **ANALYTICAL ESTIMATE** | The author's judgement, reasoned from PYQ data |
| **PREDICTION** | Forward-looking. The weakest tier |

Weightage figures marked as estimates are **Estimated Planning Weightage** for study planning only.
They are not official UPSC weightage — UPSC does not publish a subject-wise marks distribution for
this examination. PYQ counts are never manufactured; where evidence is missing, the text says so.

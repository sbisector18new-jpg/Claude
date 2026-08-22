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
| **Read the manual** | [`pdf/`](pdf/) — print-quality A4 PDFs, page-numbered. This is the version to study from |
| **Project state** | [`MASTER_CONTENT_REGISTER.md`](MASTER_CONTENT_REGISTER.md) — what is complete, what remains, study order, schedule |
| **On screen** | [`docs/index.html`](docs/index.html) — same content, reflows for phone and tablet |
| **Manuscript** | [`src/`](src/) — Markdown sources, the source of truth |

## Where the project stands

- **Complete:** all eleven modules — all **300 planning marks** covered
- **Just added:** **F11.4 — The Trap Catalogue** (Module 11) — 47 pages, 30 diagnostic questions. Thirty
  structural distractor patterns, a confusion-pair compendium, and the elimination ladder
- **Read first this cycle:** **F11.4 §5.** The four labour codes came into force on **21 November 2025**
  and the provident fund, pension and insurance schemes were replaced on **29 June 2026** — so every Act
  and scheme year previously memorised is now a distractor, while most of the *numbers* did not move
- **Still to re-supply:** Modules 1, 2, 3 and 5 into `src/`, and the 2015 and 2023 papers into `pyq/` —
  register §9. Those four modules were written against the **repealed** Acts and must be checked

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
python3 build/build.py                     # src/*.md    ->  docs/*.html
env -u NODE_OPTIONS node build/pdf.mjs     # docs/*.html ->  pdf/*.pdf
```

Both stages need no third-party packages: the HTML build is Python 3 stdlib only, and the PDF build
drives the bundled Chrome over the DevTools Protocol using Node 22's built-in WebSocket. `docs/` and
`pdf/` are generated — never edit them by hand.

`env -u NODE_OPTIONS` is required because the environment presets a `--require` hook that does not
exist on disk, which otherwise kills every `node` invocation.

PDFs are A4 with a running header, a **"Page X of Y"** footer, and `break-inside: avoid` on callouts,
tables and question blocks so no teaching unit splits across a page boundary.

> **Font note.** The only font installed here is Noto Sans, which lacks ★ → ↑ ↓ ⊂ ≈ ≠. The build
> substitutes those on the way out to HTML, and draws the star ratings as CSS shapes, so the Markdown
> sources keep the proper characters. See the register §8.2.

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

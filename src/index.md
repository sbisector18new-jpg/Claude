---
eyebrow: UPSC EPFO · ASSISTANT PROVIDENT FUND COMMISSIONER · RECRUITMENT TEST
title: APFC RT Manual
subtitle: Built documents — open any chapter, then print to PDF from your browser
version: v1.0
compiled: 16 August 2026
stage: Recruitment Test (RT)
running: APFC RT Manual · Index
---

::: action | ACTION · PDFs ARE BUILT AND READY
Every chapter is generated as a **print-quality A4 PDF** in the `pdf/` folder, with a running header,
page numbering and no page breaks through the middle of a callout, table or question block. Download
those directly — that is the version to read and print.

The HTML below is the same content for reading on screen; it reflows for phone and tablet, and you
can still print it from the browser (Ctrl/Cmd-P) if you prefer.
:::

## Available now

| Module | Chapter | Topic | PDF | On screen | Version |
|---|---|---|---|---|---|
| 6 | F6.1 | Accounting fundamentals — equation, double entry, books, trial balance and error types | [PDF, 39 pp](../pdf/module-06/F6.1-accounting-fundamentals.pdf) | [HTML](module-06/F6.1-accounting-fundamentals.html) | v1.0 |

## Project state

The **[Master Content Register](../MASTER_CONTENT_REGISTER.md)** is the source of truth for what is
complete and what remains. Read it first if you are resuming after a break.

- **Complete:** Modules 1, 2, 3, 5 — 44 chapters, 100 hours, 109.5 planning marks
- **Remaining:** Modules 4, 6, 7, 8, 9, 10, 11 — 124 hours, 190.5 planning marks

## Study order for what remains

1. **Module 6 + 7** — Accounting, Auditing, Statistics, Insurance ← in progress
2. **Module 9** — General Science & Computer Applications
3. **Module 4** — Indian Economy, Population, Development, Globalisation
4. **Module 10** — Integrated Current Affairs
5. **Module 11** — PYQ analysis, five full mocks, final revision

**Module 8** (General English, Quantitative Aptitude and Reasoning) runs *daily* alongside all of the
above, in the evening 30-minute slot — never as a block of its own. It is 80 planning marks, the
largest single block in the paper.

## Rebuilding

```
python3 build/build.py                        # src/*.md  ->  docs/*.html
env -u NODE_OPTIONS node build/pdf.mjs        # docs/*.html -> pdf/*.pdf
```

Sources live in `src/` as Markdown and are the master manuscript. Everything in `docs/` and `pdf/` is
generated — never edit it by hand.

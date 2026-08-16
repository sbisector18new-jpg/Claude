---
eyebrow: UPSC EPFO · ASSISTANT PROVIDENT FUND COMMISSIONER · RECRUITMENT TEST
title: APFC RT Manual
subtitle: Built documents — open any chapter, then print to PDF from your browser
version: v1.0
compiled: 16 August 2026
stage: Recruitment Test (RT)
running: APFC RT Manual · Index
---

::: action | ACTION · HOW TO GET A PDF
Open a chapter below, then press **Ctrl-P** (Windows) or **Cmd-P** (Mac) and choose **Save as PDF**.
The stylesheet is built for A4 and keeps callout boxes, tables and question blocks from splitting
across pages.

On a phone or tablet, use the browser's **Share → Print → Save as PDF**. The layout reflows for
narrow screens, so it stays readable without pinch-zooming.
:::

## Available now

| Module | Chapter | Topic | Version |
|---|---|---|---|
| 6 | [F6.1](module-06/F6.1-accounting-fundamentals.html) | Accounting fundamentals — equation, double entry, books, trial balance and error types | v1.0 |

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
python3 build/build.py
```

Sources live in `src/` as Markdown and are the master manuscript. Everything in `docs/` is generated —
never edit it by hand. The build needs only Python 3 and no third-party packages.

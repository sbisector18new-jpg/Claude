---
eyebrow: UPSC EPFO · ASSISTANT PROVIDENT FUND COMMISSIONER · RECRUITMENT TEST
title: APFC RT Manual
subtitle: Built documents — open any chapter as a page-numbered A4 PDF
version: v1.0
compiled: 16 August 2026
stage: Recruitment Test (RT)
running: APFC RT Manual · Index
---

::: action | ACTION · PDFs ARE BUILT AND READY
Every chapter is generated as a **print-quality A4 PDF** in the `pdf/` folder, with a running header,
**"Page X of Y"** numbering, and no page breaks through the middle of a callout, table or question
block. Download those directly — that is the version to read and print.

The HTML is the same content for reading on screen; it reflows for phone and tablet.
:::

## Module 6 — Accounting, Auditing & Statistics · complete

| Ch | Topic | PDF | On screen | Q |
|---|---|---|---|---:|
| **F6.1** | Accounting fundamentals — equation, double entry, books, trial balance, error types | [PDF, 39 pp](../pdf/module-06/F6.1-accounting-fundamentals.pdf) | [HTML](module-06/F6.1-accounting-fundamentals.html) | 40 |
| **F6.2** | Concepts, conventions, standards — and capital versus revenue | [PDF, 35 pp](../pdf/module-06/F6.2-concepts-conventions-standards.pdf) | [HTML](module-06/F6.2-concepts-conventions-standards.html) | 40 |
| **F6.3** | Final accounts, adjustments, provisions and reserves | [PDF, 28 pp](../pdf/module-06/F6.3-final-accounts.pdf) | [HTML](module-06/F6.3-final-accounts.html) | 30 |
| **F6.4** | Depreciation, goodwill and inventory valuation | [PDF, 26 pp](../pdf/module-06/F6.4-depreciation-goodwill-inventory.pdf) | [HTML](module-06/F6.4-depreciation-goodwill-inventory.html) | 30 |
| **F6.5** | Ratio analysis and cash flow | [PDF, 22 pp](../pdf/module-06/F6.5-ratios-cash-flow.pdf) | [HTML](module-06/F6.5-ratios-cash-flow.html) | 25 |
| **F6.6** | Bills of exchange and share capital | [PDF, 24 pp](../pdf/module-06/F6.6-bills-share-capital.pdf) | [HTML](module-06/F6.6-bills-share-capital.html) | 25 |
| **F6.7** | Auditing — concepts, scope, types, audit report | [PDF, 29 pp](../pdf/module-06/F6.7-auditing.pdf) | [HTML](module-06/F6.7-auditing.html) | 30 |
| **F6.8** | Statistics — central tendency, dispersion, correlation | [PDF, 21 pp](../pdf/module-06/F6.8-statistics.pdf) | [HTML](module-06/F6.8-statistics.html) | 25 |

## Module 9 — General Science & Computer Applications · in progress

| Ch | Topic | PDF | On screen | Q |
|---|---|---|---|---:|
| **F9.1** | Physics I — units, kinematics, motion, energy, fluids | [PDF, 22 pp](../pdf/module-09/F9.1-physics-mechanics.pdf) | [HTML](module-09/F9.1-physics-mechanics.html) | 30 |
| **F9.2** | Physics II — optics, heat, sound, electricity, modern physics | [PDF, 26 pp](../pdf/module-09/F9.2-physics-optics-electricity.pdf) | [HTML](module-09/F9.2-physics-optics-electricity.html) | 30 |
| F9.3 | Chemistry | — | *next* | — |
| F9.4 | Biology and environment | — | *planned* | — |
| F9.5 | Computer fundamentals and number systems | — | *planned* | — |
| F9.6 | Operating systems, software and programming | — | *planned* | — |
| F9.7 | Networking, internet and HTML | — | *planned* | — |

F9.1 and F9.2 are a **recall layer**, not a teaching layer — the blueprint is explicit that the physics
half of this module is recall rather than new learning for a Mechanical Engineer. Read the tables, then
go to the questions. Budget two days each, not four.

## Module 7 — Insurance · complete

| Ch | Topic | PDF | On screen | Q |
|---|---|---|---|---:|
| **F7.1** | Insurance — principles, types and social insurance | [PDF, 21 pp](../pdf/module-07/F7.1-insurance.pdf) | [HTML](module-07/F7.1-insurance.html) | 20 |

**245 pages, 265 practice questions**, every answer key balanced across the four options and verified
against its intended option text.

## Reading order, and the shortcuts

Read **F6.1 » F6.2 » F6.3 » F6.4** in sequence — each depends on the one before. F6.5 to F7.1 are
independent of each other and can be taken in any order.

If your time collapses, these are the sections that carry the most marks:

- **F6.1 §6** — trial balance and the four errors it cannot catch
- **F6.2 §5** — capital versus revenue, and the five one-word pairs
- **F6.3 §5 and §6** — the year-end adjustments, and provision versus reserve
- **F6.4 §2 and §5** — SLM versus WDV, and AS 2's lower of cost and net realisable value
- **F6.7 §2** — the scope of audit, the only section in Module 6 with direct PYQ evidence

## Project state

The **[Master Content Register](../MASTER_CONTENT_REGISTER.md)** is the source of truth. Read it first if
you are resuming after a break.

- **Complete:** Modules 1, 2, 3, 5, 6, 7 — 53 chapters, 130 hours, 142.5 planning marks
- **Remaining:** Modules 4, 8, 9, 10, 11 — 94 hours, 157.5 planning marks

## What to do next

1. **Module 9** — five chapters remaining: F9.3 Chemistry, F9.4 Biology, then F9.5 to F9.7 on Computer
   Applications
2. **Module 4** — Economy, lean, 8 hours
3. **Module 10** — Integrated Current Affairs
4. **Module 11** — PYQ analysis, five full mocks, final revision

**Module 8** (English, Quant and Reasoning) is **80 planning marks — the largest single block in the
paper** — and runs *daily* in the evening slot rather than as a block of its own. If it is not already
running, start it now.

## Rebuilding

```
python3 build/build.py                        # src/*.md  ->  docs/*.html
python3 build/check.py                        # quality gate
env -u NODE_OPTIONS node build/pdf.mjs        # docs/*.html -> pdf/*.pdf
```

Sources in `src/` are the master manuscript. `docs/` and `pdf/` are generated — never edit them by hand.

# APFC RT Manual — Master Content Register

**Purpose.** Single source of truth for project state across sittings. Update on every chapter
completion. Do not rely on chat history.

**Last updated:** 16 August 2026
**Exam stage:** Recruitment Test (RT) — not Interview
**Planning horizon:** RT expected late Nov / early Dec 2026 (PREDICTION — re-scale when the 2026
notification is published)

---

## 1. Ledger position

| | Modules | Chapters | Hours | Planning marks |
|---|---|---:|---:|---:|
| Complete | 1, 2, 3, 5 | 44 | 100 | 109.5 |
| **Remaining** | **4, 6, 7, 8, 9, 10, 11** | **30 + mocks** | **124** | **190.5** |
| Total | 11 | 74 | 224 | 300.0 |

Arithmetic closes against Blueprint §12 on all three columns (44+30=74 chapters, 100+124=224 hours,
109.5+190.5=300.0 marks).

**190.5 of 300 planning marks remain — roughly 64% of the paper.**

---

## 2. Completed

| M | Module | Chapters | Hours | Marks |
|---|---|---:|---:|---:|
| 1 | Indian Polity, Constitution & Governance | 13 | 28 | 32.5 |
| 2 | Labour Laws & Industrial Relations | 10 | 28 | ~30 |
| 3 | Social Security & EPFO | 11 | 22 | ~22 |
| 5 | History, Freedom Movement, Art & Culture | 10 | 22 | 25.0 |

Also complete: **Module 0 Master Blueprint v1.0**, **Foundation F1.1 v1.0** (Constitutional
Foundations), **Foundation F6.1 v1.0** (Accounting Fundamentals — in `src/`, see §8).

> **One item still unconfirmed.** Whether the **Foundation layer** (the F-prefixed, teach-from-zero
> track) was carried beyond **F1.1**. F1.1 §12 closes by naming F1.2 and F1.3 as next. If Foundation
> stopped at F1.1, then Modules 2, 3 and 5 rest on Compact-layer notes only — which is the failure
> mode F1.1 §0 was written to prevent ("memorise sentences you cannot reconstruct… they collapse
> under a *which of the following is not correct* question"). This does not block Module 6, so it is
> not on the critical path, but it should be settled before the final revision passes.

---

## 3. Remaining

Listed in recommended study order (Blueprint §10.2), not module-number order.

| Order | M | Module | Chapters | Hours | Marks | Priority |
|---:|---|---|---:|---:|---:|---|
| 1 | 6 + 7 | Accounting, Auditing & Statistics + Insurance | **7 of 8** | 30 | ~33 | ★★★★☆ |
| 2 | 9 | General Science & Computer Applications | 7 | 22 | 42.5 | ★★★★★ |
| 3 | 4 | Indian Economy + Population/Development/Globalisation | 5 | 8 | 15.0 | ★★★☆☆ |
| 4 | 10 | Integrated Current Affairs | 2 | 12 | 20.0 | ★★★★☆ |
| 5 | 11 | PYQ Analysis, 5 Mocks, Final Revision | mocks | 26 | multiplier | ★★★★★ |
| — | 8 | General English, Quant & Reasoning | 8 | 26 | **80.0** | ★★★★★ |

**Module 8 is deliberately unnumbered in that sequence.** Blueprint §10.2 item 9: English, Quant and
Reasoning are *"never a block; distributed daily practice from week 1."* It is written as drill sets
consumed in the evening 30-minute conversion slot, in parallel with whatever module is running in
the morning — not reached as a sitting of its own.

---

## 4. What the remaining work actually consists of

**Modules 8 and 9 are 122.5 of the 190.5 remaining marks — 64%.** Both are the cheapest blocks on
the board for you to convert:

- **M8 (80.0 marks)** — the single largest block in the paper, larger than Labour Laws. 2023 shape:
  10 vocabulary-in-context, 5 para jumbles, 5 comprehension on one passage; Quant is school
  mensuration, circle geometry, quadratic roots, probability, ratio, mixtures, 3 DI, heights and
  distances. Only one pure reasoning question.
- **M9 (42.5 marks)** — physics-dominated: combined lens power, inelastic collision, uniform
  acceleration, concave mirror at infinity. Per Blueprint §4.4 this is *recall, not new learning*
  for a Mechanical Engineer. Computer Applications is the exception and needs real budgeted hours
  (C, HTML, OS items), not zero.

The heavy conceptual lifting — Polity, Labour, Social Security, History — is behind you. What is
left is dominated by the fast-conversion blocks, which is the right shape for the back half of a
2-hour-a-day plan.

**Module 6 goes first anyway**, despite lower marks/hour (1.08), because Blueprint §10.1 rates it
*very high certainty* — accounting answers are definite, not judgement calls — and §10.2 places it
4th precisely because it needs uninterrupted morning attention.

---

## 5. Schedule check

Blueprint §11.3 assumed a 9 August 2026 start. Today is 16 August 2026 — **week 2 of 16**.

| | Hours | Days at 2 h/day | Calendar |
|---|---:|---:|---|
| Content (M6/7, 9, 4, 10) | 98 | 49 | ≈ 7 weeks → early October |
| Module 11 (PYQ + 5 mocks + revision) | 26 | 13 | October → RT |
| **Total remaining** | **124** | **62** | ≈ 9 weeks of study time |

Against a late-November RT this leaves genuine buffer. **Do not spend it racing ahead** — Blueprint
§11.3 is explicit that surplus time goes to mocks and the spaced-revision queue, never to new
syllabus. Module 11's 26 hours are not compressible; protect them first when work eats a week, and
sacrifice Module 4 depth first (lowest certainty, 15 marks).

---

## 6. Conventions (locked)

- Module/chapter numbering per Blueprint §12. Foundation-layer chapters prefixed **F**.
- Versions: **v1.0** at first issue, **v1.1** on revision. Never silently overwrite.
- PDFs generated automatically on chapter completion — no approval step.
- Consolidated module PDF after each module; master book after Module 11.
- **`src/` markup is the master manuscript and the source of truth. PDFs are regenerated from it.**
- `pyq/` retains the 2015 and 2023 papers for Module 11.

---

### 3.1 Module 6 chapter plan

| Ch | Topic | Status |
|---|---|---|
| **F6.1** | Accounting fundamentals: equation, double entry, books, trial balance, error types | **Complete v1.0** |
| F6.2 | Concepts, conventions, accounting standards; capital vs revenue | Next |
| F6.3 | Final accounts: trading, P&L, balance sheet; provisions and reserves | Planned |
| F6.4 | Depreciation, goodwill, inventory valuation | Planned |
| F6.5 | Ratio analysis and cash flow | Planned |
| F6.6 | Bills of exchange; share capital | Planned |
| F6.7 | Auditing concepts, scope, types, audit report | Planned |
| F6.8 | Statistics: mean, median, mode, dispersion, standard deviation | Planned |
| F7.1 | Insurance (compact): principles, indemnity, subrogation, types, role in social security | Planned |

F6.1 deliberately carries the heaviest load because everything after it depends on the equation and
the debit/credit rules. Trial balance and error types sit in F6.1 rather than later because Blueprint
§7.1 names them in the top high-yield list.

---

## 8. Build pipeline

Established this sitting. `src/` is now real, and the source-of-truth convention in §6 is live.

| Path | Role |
|---|---|
| `src/**/*.md` | **Master manuscript.** Markdown with front matter and `:::` callout blocks |
| `build/build.py` | Converter. **Python 3 stdlib only** — no third-party packages |
| `build/style.css` | Typography, callout variants, A4 print rules |
| `build/pdf.mjs` | **PDF renderer.** Drives the bundled Chrome over the DevTools Protocol. No npm packages |
| `build/shot.mjs` | Screenshot helper, for verifying layout and glyph rendering |
| `docs/**/*.html` | **Generated. Never edit by hand.** |
| `pdf/**/*.pdf` | **Generated.** A4, running header, "Page X of Y" footer |

```sh
python3 build/build.py                     # src/*.md   -> docs/*.html
env -u NODE_OPTIONS node build/pdf.mjs     # docs/*.html -> pdf/*.pdf
```

`env -u NODE_OPTIONS` is required: the environment sets
`NODE_OPTIONS=--require /opt/amazon/kiro-agent/proxy-bootstrap.js`, and that file does not exist, so
every plain `node` invocation dies with `MODULE_NOT_FOUND`.

### 8.1 How PDF generation works, and why it took a detour

There is **no** PDF toolchain here — no `pandoc`, `weasyprint`, `wkhtmltopdf` or LaTeX — and PyPI is
blocked (`403` through the proxy), so `reportlab` and `weasyprint` cannot be installed. My first
answer was that PDFs were impossible and the user should print from a browser. That was wrong.

**Chrome for Testing 151 is installed** at `/usr/local/bin/chrome`, and Node 22 ships a global
`WebSocket`. So `build/pdf.mjs` launches Chrome headless with a debugging port and calls
`Page.printToPDF` over CDP. This renders the real stylesheet and, unlike `chrome --print-to-pdf`,
supports `headerTemplate`/`footerTemplate` — which is where the page numbering comes from.

`@playwright/mcp` is installed but the Playwright **library** is not, so the CDP route is necessary
rather than merely preferred.

### 8.2 The font problem, and the fix

The only font family installed is **Noto Sans** (every weight and width, no other family). It has no
glyph for several characters the manuscript uses, so they printed as blank boxes:

| Character | Count in sources | Handling |
|---|---:|---|
| ★ ☆ priority ratings | 85 | **Drawn in CSS** with `clip-path`, so they stay real stars |
| → ← | 35 | Substituted with `»` `«` |
| ↑ ↓ | 29 | Substituted with `(+)` `(−)` |
| ⊂ ≈ ≠ | 5 | Substituted with words |

Substitution happens in `build.py` on the way out to HTML, so **the Markdown sources keep the proper
characters**. Verified: zero unrenderable codepoints remain in `docs/`.

`₹`, `—`, `·`, `§`, `−`, `…`, `÷` are all covered by Noto Sans and pass through untouched.

There is **no serif font** on the system, so headings fall back to Noto Sans rather than the serif in
the original PDFs. Cosmetic only, and it corrects itself on any machine with a serif font installed.

### 8.3 Known limitation

The table of contents has no printed page numbers — Chrome does not support CSS paged-media counters.
The TOC entries remain **clickable internal links** inside the PDF, and every page carries
"Page X of Y" in the footer.

---

## 9. Open blocker — the back catalogue

**Partly resolved.** `src/` now exists and F6.1 is in it, so new work is safe. What remains
outstanding is the **back catalogue**: Modules 1, 2, 3 and 5 are complete as study material but are
not in this repository, and neither is `pyq/`. Consequences that still stand:

1. A consolidated Module 1/2/3/5 PDF, or the final master book, **cannot be built** — the sources
   are missing, not merely unformatted.
2. A v1.1 revision of any of those chapters would mean re-authoring rather than editing.
3. Module 11 needs the 2015 and 2023 papers in `pyq/`; they are not here.

To close this, re-supply those chapters and I will bring them into `src/` in the same format.

**Output format is no longer a blocker** — see §8.1. PDFs are generated automatically from `src/`.

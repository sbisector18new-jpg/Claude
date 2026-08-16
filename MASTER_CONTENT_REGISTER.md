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
| Complete | **1, 2, 3, 5, 6, 7** | 53 | 130 | 142.5 |
| **Remaining** | **4, 8, 9, 10, 11** | **22 + mocks** | **94** | **157.5** |
| Total | 11 | 75 | 224 | 300.0 |

Arithmetic closes on all three columns (53+22=75 chapters, 130+94=224 hours, 142.5+157.5=300.0 marks).
The chapter total is 75 rather than the Blueprint's 74 because Modules 6 and 7 were delivered as **9**
chapters (F6.1–F6.8 plus F7.1) rather than the 8 originally planned — finer granularity, same content.

**157.5 of 300 planning marks remain — roughly 53% of the paper.** The halfway point is passed.

---

## 2. Completed

| M | Module | Chapters | Hours | Marks |
|---|---|---:|---:|---:|
| 1 | Indian Polity, Constitution & Governance | 13 | 28 | 32.5 |
| 2 | Labour Laws & Industrial Relations | 10 | 28 | ~30 |
| 3 | Social Security & EPFO | 11 | 22 | ~22 |
| 5 | History, Freedom Movement, Art & Culture | 10 | 22 | 25.0 |
| **6** | **Accounting, Auditing & Statistics** | **8** | **26** | **~30** |
| **7** | **Insurance** | **1** | **4** | **~3** |

Also complete: **Module 0 Master Blueprint v1.0**, **Foundation F1.1 v1.0** (Constitutional
Foundations), **Foundation F6.1 v1.0** (Accounting Fundamentals) and **Foundation F6.2 v1.0**
(Concepts, Conventions, Standards, Capital vs Revenue). F6.1 and F6.2 are in `src/` with PDFs — see §8.

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
| 1 | 9 | General Science & Computer Applications | **5 of 7** | 22 | 42.5 | ★★★★★ |
| 2 | 4 | Indian Economy + Population/Development/Globalisation | 5 | 8 | 15.0 | ★★★☆☆ |
| 3 | 10 | Integrated Current Affairs | 2 | 12 | 20.0 | ★★★★☆ |
| 4 | 11 | PYQ Analysis, 5 Mocks, Final Revision | mocks | 26 | multiplier | ★★★★★ |
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
| **F6.1** | Accounting fundamentals: equation, double entry, books, trial balance, error types | **Complete v1.0** — 39 pp, 40 Q |
| **F6.2** | Concepts, conventions, accounting standards; capital vs revenue | **Complete v1.0** — 35 pp, 40 Q |
| **F6.3** | Final accounts; adjustments; provisions and reserves | **Complete v1.0** — 28 pp, 30 Q |
| **F6.4** | Depreciation, goodwill, inventory valuation | **Complete v1.0** — 26 pp, 30 Q |
| **F6.5** | Ratio analysis and cash flow | **Complete v1.0** — 22 pp, 25 Q |
| **F6.6** | Bills of exchange; share capital | **Complete v1.0** — 24 pp, 25 Q |
| **F6.7** | Auditing: concepts, scope, types, audit report | **Complete v1.0** — 29 pp, 30 Q |
| **F6.8** | Statistics: central tendency, dispersion, correlation | **Complete v1.0** — 21 pp, 25 Q |
| **F7.1** | Insurance (compact): principles, types, role in social security | **Complete v1.0** — 21 pp, 20 Q |

**245 pages, 265 questions.** Depth was scaled to yield rather than spread evenly: F6.1 and F6.2 carry
the heaviest load because everything after them depends on the equation and the debit/credit rules;
F6.5 and F6.6 are deliberately leaner as ★★★☆☆ topics; F7.1 is compact because Blueprint §7.2 places
insurance in the low-yield list at one question in 2023.

F6.7 §2 (scope of audit) is the only section in the module with **direct PYQ evidence** — the 2023 paper
tested it through a "which one is not correct" item.

### 3.2 Module 9 chapter plan — in progress

This module was **added on the Blueprint's recommendation** (§9.1), which called it the single correction
worth more marks than any other change available. It is **official syllabus head 6**, appeared in every
paper analysed, and was worth **50 marks in 2023** — as much as the entire labour block.

The plan is built directly onto the ten 2023 General Science items and ten Computer Applications items
recorded in Blueprint §4.4, so every known PYQ maps to a chapter:

| Ch | Topic | 2023 items it answers | Status |
|---|---|---|---|
| **F9.1** | Physics I: units, kinematics, motion, energy, fluids | Inelastic collision; uniform acceleration of a train | **Complete v1.0** — 27 pp, 30 Q |
| **F9.2** | Physics II: optics, heat, sound, electricity, modern physics | Combined lens power; concave mirror at infinity | **Complete v1.0** — 28 pp, 30 Q |
| F9.3 | Chemistry | Effluents and pH; soaps; an enthalpy reaction | Next |
| F9.4 | Biology and environment | Eyeball layers; banyan prop roots; ocean acidification | Planned |
| F9.5 | Computer fundamentals and number systems | Octal to binary; hexadecimal to decimal; program counter register | Planned |
| F9.6 | Operating systems, software and programming | Real-time OS; top-down languages; C structure operator; HDD error-check command | Planned |
| F9.7 | Networking, internet and HTML | IP address validity; mesh topology links; HTML internal linking | Planned |

**Chapters F9.1 and F9.2 are deliberately written as a RECALL layer, not a teaching layer.** Blueprint
§9.1 states that the physics half is *"not new learning — it is recall"* for a Mechanical Engineer, so
teaching it from first principles would spend the hours the Blueprint exists to save. They are dense
tables, formulas, traps and heavy practice, budgeted at two days each rather than four.

Blueprint §4.4 also warns that **Computer Applications is the exception** — number-system conversions
are easy, but the C, HTML and operating-system items *"need actual targeted preparation. Budget real
hours there, not zero."* F9.5 to F9.7 will therefore be written as a genuine Foundation layer, not a
recall layer.

---

## 8. Build pipeline

Established this sitting. `src/` is now real, and the source-of-truth convention in §6 is live.

| Path | Role |
|---|---|
| `src/**/*.md` | **Master manuscript.** Markdown with front matter and `:::` callout blocks |
| `build/build.py` | Converter. **Python 3 stdlib only** — no third-party packages |
| `build/style.css` | Typography, callout variants, A4 print rules |
| `build/pdf.mjs` | **PDF renderer.** Drives the bundled Chrome over the DevTools Protocol. No npm packages |
| `build/check.py` | **Quality gate.** Run before every commit — see §8.4 |
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

The substitution map was extended while writing F6.8: **≥ ≤ √ ∞ ∑** are also absent from Noto Sans.
Note the odd case — Greek capital sigma **Σ** (U+03A3) *is* present while the n-ary summation **∑**
(U+2211) is not, so the build maps one to the other. Greek σ, μ and ρ, the superscript two, ± and × are
all fine.

### 8.4 The quality gate

`python3 build/check.py` runs before every commit and checks each chapter for:

1. Question numbering contiguous from 1
2. An answer row for every question
3. **Answer key balance** across the four options — a key that never uses one letter lets a candidate
   score by elimination and trains the wrong instinct
4. **Section-heading numbering contiguous** — this caught a real defect immediately, F6.4 having jumped
   from section 5 to section 7
5. No unrenderable codepoints surviving into the built HTML

All nine Module 6 and 7 chapters pass. Keys: F6.1 and F6.2 at 10/10/10/10, F6.3 8/7/8/7, F6.4 8/8/7/7,
F6.5 6/7/6/6, F6.6 6/6/7/6, F6.7 7/8/7/8, F6.8 7/6/6/6, F7.1 5/5/5/5.

### 8.5 Known limitation

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

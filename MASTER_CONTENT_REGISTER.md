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
| Complete (reported) | 1, 2, 3 | 34 | 78 | 84.5 |
| **Remaining** | **4, 5, 6, 7, 8, 9, 10, 11** | **40 + mocks** | **146** | **215.5** |
| Total | 11 | 74 | 224 | 300.0 |

**215.5 of 300 planning marks are still unwritten — roughly 72% of the paper.** The completed
Polity/Labour/Social-Security core is the highest-certainty block, but it is not the highest-marks
block.

---

## 2. Completed

| M | Item | Status | PDF | Version |
|---|---|---|---|---|
| 0 | Master Blueprint (Modules 1–11) | Complete | Yes | v1.0 |
| 1 | Foundation F1.1 — Constitutional Foundations | Complete | Yes | v1.0 |
| 1 | Compact Ch 1.1–1.13 | Reported complete | — | — |
| 1 | Foundation F1.2–F1.13 | **Status unconfirmed** | — | — |
| 2 | Ch 2.1–2.10 | Reported complete | — | — |
| 3 | Ch 3.1–3.11 | Reported complete | — | — |

> **Open question blocking a clean register.** Only the Blueprint v1.0 and Foundation F1.1 v1.0 are
> verifiable (both supplied as PDFs). Modules 1–3 are recorded as complete because they are absent
> from the remaining-work list, not because I can see them. F1.1 closes by naming F1.2 and F1.3 as
> "next in the Foundation track", so it is unclear whether the Foundation layer was carried through
> all of Module 1 or stopped at F1.1. **Confirm before Module 5 begins**, because if the Foundation
> layer stops at F1.1 then Modules 2 and 3 rest on Compact-only notes — which is the exact failure
> mode Foundation F1.1 §0 was written to prevent.

---

## 3. Remaining — in your stated order

| M | Module | Chapters | Hours | Marks | Priority |
|---|---|---:|---:|---:|---|
| 5 | History, Freedom Movement, Art & Culture | 10 | 22 | 25.0 | ★★★★☆ |
| 6 | Accounting, Auditing & Statistics | 8 combined | 26 | ~30 | ★★★★☆ |
| 7 | Insurance (compact) | ↑ with M6 | 4 | ~3 | ★★☆☆☆ |
| 8 | General English, Quant & Reasoning | 8 | 26 | **80.0** | ★★★★★ |
| 9 | General Science & Computer Applications | 7 | 22 | 42.5 | ★★★★★ |
| 4 | Indian Economy + Population/Development/Globalisation | 5 | 8 | 15.0 | ★★★☆☆ |
| 10 | Integrated Current Affairs | 2 | 12 | 20.0 | ★★★★☆ |
| 11 | PYQ Analysis, 5 Mocks, Final Revision | mocks | 26 | multiplier | ★★★★★ |

---

## 4. Two sequencing problems in that order

**4.1 Module 8 is 80 marks and is last-but-three.** It is the single largest block in the paper —
larger than Labour Laws. Blueprint §10.2 item 9 is explicit that English, Quant and Reasoning are
"never a block; distributed daily practice from week 1". Treating M8 as a sitting to be reached
later contradicts the plan it came from. **Write its drill sets early and consume them daily in the
evening 30-minute slot**, rather than queuing the module behind History.

**4.2 History before Accounting and Science inverts the marks-per-hour order.** Blueprint §10.2
sequences Accounting (4th) and Science/Computers (5th) *ahead of* History (6th), because History has
the lowest certainty of return per hour in the whole table (1.14 marks/hr, certainty Low, capped at
22 hours) while Accounting and Science are high-certainty converters.

**Recommended resequence:** 6/7 Accounting → 9 Science & Computers → 5 History → 4 Economy →
10 Current Affairs → 11 Mocks, with 8 running daily throughout from now.

---

## 5. Schedule reality check

Blueprint §11.3 assumed a 9 August 2026 start. Today is 16 August 2026 — **week 2 of 16**.

- Remaining content: 146 hours ÷ 2 hours/day ≈ **73 study days ≈ 10.5 weeks**
- Leaves roughly 3 weeks of buffer before a late-November RT
- **Module 11's 26 hours are not compressible.** Five full mocks plus PYQ re-solve plus error-log
  review is the multiplier on everything above it. Protect it first when work eats a week; sacrifice
  History depth and Economy, per Blueprint §10.1.

---

## 6. Conventions (locked)

- Module/chapter numbering per Blueprint §12. Foundation-layer chapters prefixed **F**.
- Versions: **v1.0** at first issue, **v1.1** on revision. Never silently overwrite.
- PDFs generated automatically on chapter completion — no approval step.
- Consolidated module PDF after each module; master book after Module 11.
- **`src/` markup is the master manuscript and the source of truth. PDFs are always regenerated
  from it.** ⚠️ `src/` does not currently exist in this repository — see §7.
- `pyq/` retains the 2015 and 2023 papers for Module 11. ⚠️ Also absent.

---

## 7. Continuity risk — open

Nothing from the earlier sitting is present in this repository: no `src/`, no `pyq/`, no chapter
markup. The Blueprint and Foundation F1.1 exist only as PDFs supplied in chat. Consequences:

1. Consolidated module PDFs and the master book **cannot be regenerated** from source.
2. Revisions (v1.1) would mean re-authoring, not editing.
3. The convention in §6 that `src/` is the source of truth is currently aspirational.

**Fix before writing new material:** commit chapter markup to `src/` as each chapter is written, and
push after every sitting. From this register onward, every deliverable lands in the repo first and is
rendered to PDF second.

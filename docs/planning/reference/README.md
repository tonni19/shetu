# Reference material

Copies of the files our planning documents rely on, so this folder works on its own. **Read-only:** do not edit these; they are sources, not our work in progress.

## `course-documents/`

What the faculty gave us. Every requirement in `../02-Requirements-Traceability-Checklist.md` points to one of these.

| File | What it is |
|---|---|
| `Course Outline.pdf` | Official syllabus: marks, lab sequence, course outcomes. Note: it says Section C and Summer 2026, so day, room and dates may not apply to us (report, section 2.6) |
| `Lab Manual.pdf` | Class 01 slides: the project rules (AI at the core, GitHub, Selenium, Project Show) |
| `Lab Manual 2.pdf` | Class 02 slides: kinds of software, role-based access, audit trails, payments |
| `Project Pitch Presentation.docx` | The five instructions for the proposal presentation |
| `SE LAB SECTION E PROJECT TEAM.xlsx` | The original faculty workbook (our filled version is `../04-Workbook-Submission-Draft.xlsx`) |

## `competition/`

From GP FutureMakers 2026, where Shetu started. Useful for background and verified statistics. **Some claims here are outdated or inaccurate**; check `../01-Investigation-Report.md`, section 3.5, before reusing any.

| File | What it is |
|---|---|
| `HANDOFF - Shetu Round 2.md` | Status notes from the competition. **Section 5 has the fact-checked statistics with sources**; use only those figures |
| `1. Shetu Product Brief.docx` | The competition product description |
| `Shetu_Round2_FutureMakers.pdf` / `.pptx` | The competition deck. Our proposal deck copies its visual style |

## `brand/`

The Shetu logo in colour and in white. The deck's colours are crimson `BF092F`, cream `F8F4EC` and ink `222023`, with the font Plus Jakarta Sans.

## `competition-prototype/`

The source code of the competition prototype, without the 3.3 GB model file and binaries. **It is not our lab project.** It ran once on one hand-written case (Nusrat) and its screens were mostly static. The investigation report audits it in sections 3 to 5.

Worth reusing as ideas or starting points:

| File | Useful part |
|---|---|
| `engines/handover.py` | Checks that every number in an AI answer appears in her words; converts Bangla number words to digits |
| `engines/return_plan.py` | `parse_clock`: reads times like "sondha 6 ta" or "6 o'clock evening" by rule, not by AI |
| `engines/qa.py` | Answers questions only from the handover, and refuses when it cannot cite a source |
| `engines/shetu.py` | Role Map extraction prompt, job description cross-check, fix proposals checked by rules |
| `engines/llm.py` | How the local model was called |
| `demo/nusrat.json`, `demo/results.json` | The demo case and its one saved AI output |

Not worth reusing: the Flask screens (we use React now), and the fixed 60/80/100% return logic in `return_plan.py` (we decided against fixed percentages).

# AGENTS.md: context for AI assistants reading this folder

You are helping a member of **Team Anomaly** (four undergraduate students at UIU) with **Shetu**, their Software Engineering Lab project (CSE 3422). This folder (`docs/planning/`) is the **planning folder**: decisions, the proposal deck and Excel sheet, and reference material. It contains no application code. The application is built in this same repository; the root `AGENTS.md` has the coding rules, and `docs/PROJECT-STATE.md` has the current state.

## Read before answering

1. `00-Overview.md`: the current decisions, in plain words. Treat it as the source of truth.
2. `CHANGELOG.md`: what changed recently.
3. The relevant section of `01-Investigation-Report.md` for detail. Sections 19 to 26 are the latest. Where an older section (1 to 18) and a newer one disagree, the newer one wins.

## Key facts

- **Product:** Shetu keeps an employee's job intact through a long leave, starting with maternity leave. Three stages: **MAP** (before leave: AI interview, evidence-backed Role Map, handover plan), **HOLD** (during leave: colleagues hold duties; a change typed in plain words is understood and re-planned), **FIT** (return: clashes found by rules, fixes proposed by AI).
- **Hourglass Model:** the shape of a leave. Duties pass to colleagues before leave and come back after. It is an ownership timeline (every duty has an owner on every date), not extra stages, and there are no fixed workload percentages.
- **Core rule:** AI proposes, rules check, people decide.
- **Stack:** FastAPI (Python) backend, React frontend, SQLite, pytest and Selenium, GitHub.
- **AI model:** hosted model through a provider-independent gateway; local Qwen3-4B as fallback. The provider is **not chosen**; it will be decided by testing on fake cases.
- **Status:** planning only. **No lab code exists.** The proposal presentation is on 15 November 2026.

## Rules for you

- Do not present planned features as built. The competition prototype in `reference/competition-prototype/` only worked on one scripted case.
- Do not invent evaluation results, user research, or team decisions. If something is not in these files, say so.
- Fake data only. Never suggest using real employee data.
- The member must be able to explain everything you help produce. Explain in simple terms, and teach rather than just hand over answers.
- Do not reuse names, numbers or claims from `reference/competition/` without checking them against `00-Overview.md`; some competition claims were found to be inaccurate (report, section 3.5).
- If you change a decision document, also add an entry to `CHANGELOG.md`.

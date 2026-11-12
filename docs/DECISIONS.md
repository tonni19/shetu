# Decisions

Settled questions and why. Add a row when a decision is made. Do not re-open one without a new Issue.

| # | Date | Decision | Why |
|---|---|---|---|
| 1 | 2026-11-12 | Product direction is the "Shetu Evidence Map": Map, Hold, Fit around one evidence-backed Role Map | Makes AI necessary in all three stages; one coherent product |
| 2 | 2026-11-12 | Every duty has a status: said, documented or suggested. Suggested items are questions until a person confirms | Separates fact from AI guess |
| 3 | 2026-11-12 | The hourglass is modelled as an ownership timeline: every duty has an owner on every date. No fixed workload percentages | Plans are agreed person by person; percentages are a result, not a setting |
| 4 | 2026-11-12 | AI proposes, rules check, people decide. Dates, times, numbers and capacity are computed by code | Small models got dates and times wrong in the prototype |
| 5 | 2026-11-12 | Backend FastAPI, frontend React, database SQLite | Instructor's advice; clean split for a four-person team; Pydantic fits AI output validation |
| 6 | 2026-11-12 | All model calls go through one gateway with swappable providers | Change provider without rewriting the app; local model for private use |
| 7 | 2026-11-12 | Hosted model is primary, local Qwen3-4B is fallback, Colab is for experiments only | Team-wide access; Colab can disconnect at any time |
| 8 | 2026-11-12 | The hosted provider is chosen by a bake-off on synthetic scenarios | Quality on Banglish cannot be judged from documentation |
| 9 | 2026-11-12 | Synthetic data only | The subject is sensitive; free model tiers may use submitted data |
| 10 | 2026-11-12 | Not building: voice, live integrations, autonomous agents, scoring of people, payments | Scope and ethics |
| 11 | 2026-11-12 | No LangChain, agent frameworks, vector databases, Redux or Next.js | We must be able to explain every part |
| 12 | 2026-11-12 | The roadmap in `docs/planning/00-Overview.md` section 7 is final; three simplifications apply from day one (FIT checks time clashes only, the AI compares against the job description only, a simple HR approval list) | React + FastAPI adds work to an already tight plan |
| 13 | 2026-11-12 | This repository is the single source of truth: plan in `docs/planning/`, code at the root | Everyone, and every AI assistant, reads the same files |
| 14 | 2026-11-12 | Any member with write access may review and merge a pull request, using their own GitHub account, but never their own pull request. Merge with a **merge commit**, not squash | Reviews and merges are recorded under the real person; squash would hide each member's own commits |
| 15 | 2026-11-12 | Until `main` can be protected, "no direct pushes to `main`" is kept by agreement. Branch protection needs GitHub Pro on the repository owner's account | Free private repositories do not allow branch protection; `tonni19` owns the repository |

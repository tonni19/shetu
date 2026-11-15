# Shetu, explained: the interactive learning guide

Online: **https://tonni19.github.io/shetu/** (updated automatically a minute or two after a change to `docs/learn` is merged into `main`). Offline: open **`index.html`** in any browser (double-click it after you pull).

The online page is **public**, even though the repository is private. Never add student IDs, emails, keys or course material to this folder. It works offline, needs nothing installed, and saves your progress in your own browser only.

It teaches the whole project in 14 short lessons: the problem, Map / Hold / Fit, the hourglass, evidence, who does what (AI, rules, people), the HOLD re-planning flow, how the app is built, the AI gateway, how we measure the AI, privacy, GitHub teamwork, who builds what, the course and the presentation, and a final exam. It has simulators, sorting games, quizzes and a glossary.

A second group, **Deeper, in plain words**, explains the technical words in more detail: what a rule is, tests and pytest, the architecture piece by piece, the AI pipeline, tokens and embeddings, and our niche (why maternity first, and why Shetu is not a work planner). Anything there that the team has not agreed is marked "Proposed, not agreed".

**Add to it whenever something is explained.** If a teammate's assistant teaches a concept about Shetu, put the explanation in the guide too, so the whole team can read it later.

## Keep it true

The guide teaches the **plan**. When a decision or the design changes, update the matching lesson in the same pull request, the same way you update `docs/PROJECT-STATE.md`. When something is actually built, change the lesson's wording from "planned" to "built" and say where the code is. Never let the guide say something is built when it is not.

## How it is made

One self-contained HTML file: the text, the styles, the Plus Jakarta Sans font (subset, embedded) and plain JavaScript are all inside it. No libraries, no network. Edit it as a normal text file. The lessons are the `<section class="lesson">` blocks, the quiz questions are the `QB` object near the top of the script, and the glossary is the `GLOSS` list.

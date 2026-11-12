# Interactive learning guide

- Prepared by: Ahmad Maruf Hossain, with an AI assistant
- Branch: `feature/learning-guide` (rename to `feature/<issue number>-...` if an Issue is opened)
- Date: 2026-11-13

## What was done
Added `docs/learn/index.html`: one offline page that teaches the whole project in 14 lessons with simulators (ownership timeline, HOLD re-planning, the AI gateway, grading the AI, a merge-conflict fix), sorting games, quizzes, flashcards of likely instructor questions, a 20-question final exam and a glossary. Added `docs/learn/README.md`, a line in the repo README, a note in `AGENTS.md`, decision 18 and an AI-USAGE line.

## Why
The team asked to be taught everything, in something better than Markdown files. Everyone must be able to explain the project, and the course grades that.

## How it works
A single HTML file with the text, styles, an embedded subset of Plus Jakarta Sans, and plain JavaScript. Progress is saved in the browser's localStorage only. The simulators use pre-written data: they illustrate the design and are not the real system. The widgets are in the `W` object in the script; quiz questions are in `QB`; glossary in `GLOSS`.

## How it was tested
In headless Chrome with Playwright: every lesson loads with no JavaScript errors; 31 checks click through each widget, all 48 gateway combinations, every quiz, the exam, saved progress after a reload, and a phone-width layout with no sideways scrolling. Not tested on Safari or Firefox.

## Not finished / known problems
- Content reflects the plan on 13 November 2026 and will go stale unless it is updated with the design (see the rule in `AGENTS.md`).
- The simulators' numbers (hours, names) are illustrative.
- Nobody else has read the lessons yet. Teammates should check the ones about their own area.

## AI assistance
Claude Code designed and wrote it; the member reviewed it. Recorded in `AI-USAGE.md`.

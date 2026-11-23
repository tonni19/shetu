# Shetu (সেতু)

An AI system that keeps a job intact through a long leave. Software Engineering Lab project (CSE 3422, Section E), United International University.

**Team Anomaly:** Sadia Noman Tonni · Nazha Tarannum Roza · Ahmad Maruf Hossain · Mohammad Mahadi Hasan

## What it does

When an employee goes on a long leave, nobody holds a full picture of her job. Shetu manages the whole leave in three stages:

| Stage | What happens |
|---|---|
| **MAP** (before leave) | An AI interview in Bangla, English or Banglish builds a map of her real duties, each with evidence, finds duties she forgot, and plans who takes each one |
| **HOLD** (during leave) | Colleagues hold her duties. When something changes, the manager says so in plain words and the AI proposes a new plan |
| **FIT** (return) | She states the arrangement she needs. Rules find clashes; the AI proposes fixes |

AI proposes, rules check, people decide.

## Status

**Proposal presented on 15 November 2026.** Team Anomaly is preparing a running foundation and the first slice of the MAP flow for the progress presentation on Thursday, 26 November. See [the current state](docs/PROJECT-STATE.md) and [the Update 1 plan](docs/UPDATE-1-PLAN.md).

## Start here

| If you want to... | Read |
|---|---|
| Understand the whole project quickly | [docs/planning/00-Overview.md](docs/planning/00-Overview.md) |
| See the proposal slides | [docs/planning/05-Shetu-Proposal-Deck.pdf](docs/planning/05-Shetu-Proposal-Deck.pdf) |
| Learn the whole project, interactively (best first step for everyone) | Open https://tonni19.github.io/shetu/ (or [docs/learn/index.html](docs/learn/index.html) after pulling) |
| Know what is done and what is next | [docs/PROJECT-STATE.md](docs/PROJECT-STATE.md) |
| Build or rehearse the first checkpoint | [docs/UPDATE-1-PLAN.md](docs/UPDATE-1-PLAN.md) |
| Write code with an AI assistant | [AGENTS.md](AGENTS.md) first, always |
| Know why something was decided | [docs/DECISIONS.md](docs/DECISIONS.md) |

## Repository layout

```
AGENTS.md            Briefing and rules for AI assistants (CLAUDE.md points here)
AI-USAGE.md          Where AI tools were used (course requirement)
docs/
  PROJECT-STATE.md   What works, who is doing what, what is next. Updated in every pull request
  UPDATE-1-PLAN.md   First checkpoint scope, proposed owners, schedule and handoff
  DECISIONS.md       Settled decisions and their reasons
  worklog/           One short note per pull request
  learn/             Interactive learning guide: open index.html in a browser
  planning/          The full plan: overview, investigation report, pitch pack, slides, Excel draft
    reference/       Course documents, competition materials, logos, old prototype code
.github/             Pull request template
backend/             FastAPI app (not created yet)
frontend/            React app (not created yet)
```

## Tech stack

Python and FastAPI (backend), React (frontend), SQLite, pytest and Selenium. The AI model is reached through our own gateway, so the provider can be changed.

## How we work

1. Pull `main` before you start.
2. If you use an AI assistant, have it read [AGENTS.md](AGENTS.md) and [docs/PROJECT-STATE.md](docs/PROJECT-STATE.md) first.
3. One Issue, one branch, one pull request, reviewed by a teammate. Nobody pushes straight to `main`.
4. Every pull request adds a worklog note and updates the project state. See [docs/worklog/README.md](docs/worklog/README.md).
5. Commit from your own GitHub account, and be able to explain your own code.

## Data

All data in this repository is synthetic. No real employee information is used.

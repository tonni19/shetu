# Deck fixes 1 to 5 and a refresh of the project state

- Prepared by: Ahmad Maruf Hossain, with an AI assistant
- Branch: `feature/deck-fixes-and-state`
- Date: 2026-11-14

## What was done
Applied the five accuracy fixes from `docs/planning/06-Slide-Deck-Change-Proposals.md` (items 1 to 5) to the slide deck, and exported the PDF again. Changed the learning guide's wording of the bank statistic to match. Refreshed `docs/PROJECT-STATE.md`, which was out of date again: it still listed two finished Issues as in progress, did not list pull requests #8, #9, #10 and #12, and said the instructor had not replied. Added decision 19.

## Why
The proposals came from a read of the deck the day before the presentation. Each one stops a slide claiming more than we can show. The project state has to match reality (rule in `AGENTS.md`).

## How it works
The deck is built from a script that is not in this repository, so the new `.pptx` and PDF replace the old ones as files. The slide text changes are listed in `docs/planning/CHANGELOG.md`.

## How it was tested
The deck was rendered through PowerPoint and the changed slides (2, 3, 5, 8, 9) were checked by eye for overflow. The learning guide was rebuilt and its 31 browser checks pass.

## Elevator speech
The team's final elevator speech (written by Tonni) was added unchanged to the workbook cell E3, the pitch pack and the notes of slide 1. Words were not edited. One line describes a design option, not what the lab version does: "all data stays on the company's own server". The team decided to keep the wording, and the pitch pack has a prepared answer. The team also agreed the speaker split (decision 21).

## Not finished / known problems
- Items 6 to 9 in the proposals file are optional and not applied.
- Whether the Excel sheet was entered in the faculty's Google Sheet is not recorded.
- Pull requests #4 to #12 were merged without a recorded review. Where a merge was done from Maruf's computer under another member's account, the project state says so.

## AI assistance
Claude Code made the changes; the member reviewed the rendered slides. Recorded in `AI-USAGE.md`.

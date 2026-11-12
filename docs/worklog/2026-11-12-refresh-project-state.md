# Refresh the project state and add a rule to keep it current

- Prepared by: Ahmad Maruf Hossain, with an AI assistant
- Pushed and opened as: `tonni19`, at the team's request. Merged by `SpicyFalcon619`, who is not the pull request's author
- Branch: `feature/7-refresh-project-state`
- Date: 2026-11-12

## What was done
Brought `docs/PROJECT-STATE.md` up to date: PRs #4 and #6 merged, nothing else open, voice is a stretch feature, Tonni's student application approved (benefits due about 15 November), the work-division proposal, and the Jira question. Added a rule to `AGENTS.md` ("Keep the project state current"), a line in the pull request template, and decision 17.

## Why
The state file was a few hours old and already wrong: it listed an open PR that had been merged and said Tonni's Pro was not started. Every teammate's AI assistant reads this file first, so a stale file means wrong advice.

## How it works
Documents only. The new rule lists what counts as a change (merge, decision, access, plan, instructor feedback, blocker, milestone), says to update in the same PR or a small PR the same day, and tells assistants to write only what they verified.

## How it was tested
Not applicable. Each statement was compared with GitHub: merged and open PRs, issues, collaborators, and the education page.

## Not finished / known problems
- "Merged so far" always lags by one PR, because a merge cannot be recorded inside its own PR. The rule covers this with a same-day follow-up PR, and the file says so.
- Whether the instructor email was sent is not recorded.
- No teammate other than the merger has read this change.

## AI assistance
Claude Code compared the file with reality and drafted the rule; the member reviewed it. Recorded in `AI-USAGE.md`.

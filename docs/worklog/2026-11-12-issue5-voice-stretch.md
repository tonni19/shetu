# Issue #5: Voice input is a stretch feature

- Author: Ahmad Maruf Hossain
- Branch: `feature/5-voice-is-a-stretch-feature` (built on top of PR #4's branch; merge #4 first)
- Date: 2026-11-12

## What I did
Made the documents agree about voice input. The report and pitch pack said it was a stretch feature, but the overview, the plan slide and the summary written for the instructor said it was dropped. Now all say: stretch, first in line after HOLD works. Added decision 16 and a note on a cheaper way to build it.

## Why
A team member pointed out that voice was a main selling point in the competition. It was not meant to be removed, only postponed.

## How it works
Documents and slides only. Planned approach for later: record audio in the browser, send it to the backend, and let the AI gateway pass it to the same hosted model for transcription. Not built.

## How I tested it
Not applicable. I searched all planning documents for "voice" and checked each mention.

## Not finished / known problems
- The 6 to 12 hour estimate for voice is a guess. Whether the chosen model understands spoken Bangla well enough is untested.

## AI assistance
Claude Code found the inconsistency and drafted the changes; I reviewed them. Recorded in `AI-USAGE.md`.

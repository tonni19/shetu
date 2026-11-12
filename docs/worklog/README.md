# Worklog

One short file per pull request. This is how the next person, and their AI assistant, learns what you did.

**File name:** `YYYY-MM-DD-issue<number>-short-name.md`, for example `2026-11-20-issue12-interview-screen.md`.

Separate files are used on purpose: if everyone edited one shared log, git would produce merge conflicts.

## Template

```markdown
# <Issue number and title>

- Author: <your name>
- Branch: <branch name>
- Date: <YYYY-MM-DD>

## What I did
Two to five plain sentences.

## Why
The reason, if it is not obvious from the Issue.

## How it works
The data flow in a few lines. Which parts call the AI and which are ordinary code.

## How I tested it
Tests added, and what I checked by hand.

## Not finished / known problems
What the next person must know.

## AI assistance
Which tool helped, with what, and what I checked or changed myself.
```

Keep it short and true. A wrong note is worse than no note.

# 2026-11-23: Coordination rules and the team board

- Author: Maruf
- Branch: `feature/coordination-rules`
- Date: 2026-11-23

## What I did
Added the rules and files that let four people and their AI assistants build dependent parts without stepping on each other: `docs/TEAM-BOARD.md` (owners, dependencies, status, handoff log), `docs/API-CONTRACT.md` (proposed shared data shapes, routes and function signatures), and two new sections in `AGENTS.md` ("Coordinate before you act" and "Comments for the next AI"). The pull request template and the "finished" checklist were extended to match.

## Why
Every member works with an AI that remembers nothing between sessions. When one person's part needs another's (for example the interview route needs the gateway and the rules), the AI has to check what is really merged, use a labelled stub if it is not, and never guess names that other parts depend on.

## How it works
At the start of a session the AI runs `git fetch`, reads the state, the board and the contract, and checks each dependency on `origin/main`. It then builds, stubs or stops and reports. Shared interfaces change only through a pull request that edits the contract and logs a handoff for the affected people. Code carries a header and `AI NOTE:`, `STUB(T#)`, `TODO(owner, T#)`, `CONTRACT:` and `SECURITY:` comments so the next AI understands it without asking.

## How I tested it
Documentation only. Read the new rules against the existing ones for contradictions: none found. The board rows match the Thursday plan in `docs/UPDATE-1-PLAN.md`.

## Learning guide
The "Who builds what" lesson now shows the four confirmed owners by name (it still described four unassigned areas, A to D). The quiz question about who owns HOLD was replaced by one about who owns the gateway, and the architecture widget names owners instead of letters.

## Not finished / known problems
- The owners on the board are confirmed (all four members accepted on 23 November 2026, reported by Maruf).
- The contract is proposed, not agreed. It must be agreed by all four owners before it is called final.
- No application code yet, so the comment standard has not been used on real files.

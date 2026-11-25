# Issue #28: T2 frontend skeleton (sign-in and the case page)

- Author: Sadia Noman Tonni
- Branch: feature/28-frontend-skeleton
- Date: 2026-11-25

## What I did
Created the React app in `frontend/` with Vite, TypeScript and React Router 8. It has a sign-in screen (a user id and password form, plus one-click buttons for the synthetic demo accounts) and a case page. The case page reads `GET /api/cases/{id}` from the real backend and shows the leave dates, the stage (Map, Hold, Fit) and the Role Map, with each duty's evidence and confirmation kept apart. There are clear screens for 401, 403, 404 and a server that cannot be reached. The look follows the learning guide (same colours, font and bridge mark).

## Why
T2 on the board, for the progress presentation on Sunday 29 November. I chose TypeScript over plain JavaScript as the better fit: the screens and the API must agree on every field, and the type checker catches a missing or invented field (for example a reason for leave) or a forgotten `null` before the app runs. Decision 32; the team still has to confirm the new development libraries on Issue #28.

## How it works
`src/session.tsx` asks `GET /api/me` at start-up. The guard in `src/App.tsx` sends a signed-out person to `/sign-in` and back afterwards. Sign-in uses `POST /api/login`, and the server sets a signed, HttpOnly cookie that JavaScript cannot read. `src/pages/CasePage.tsx` calls `GET /api/cases/{id}` through `src/api/client.ts`. The Vite proxy (`vite.config.ts`) forwards `/api` to the backend, so the browser sees one site and sends the cookie. No AI runs in the frontend; everything here is ordinary code. Details: `docs/CODE-EXPLANATION.md`, "Frontend skeleton".

## How I tested it
No automated frontend test tool is agreed yet (Vitest is proposed on Issue #28). Checks run on 25 November:
- `npm run typecheck` and `npm run build` pass. The checker was shown to catch two deliberate mistakes: an unhandled null `hours_per_week`, and a non-existent `reason` field.
- `python -m pytest` from the repository root: 30 passed, after merging the latest `main` (with T7).
- In a real browser (Playwright), against the real backend:
  - signed out on `/cases/case-1`: sent to sign-in;
  - wrong password: "The user id or password is wrong." and you stay on the sign-in page;
  - right password: back to `/cases/case-1`, with two duties, 172 days, Map current;
  - the employee opening `case-2`: "You cannot open this case" (403 from the server);
  - `case-99`: "Case not found"; an unknown address: "Page not found";
  - the manager on `case-2`: "Manager: You", 59 days;
  - reload keeps the session;
  - a cover colleague: 403;
  - an expired session (cookie deleted): sign in returns to the same page;
  - no localStorage or sessionStorage used; `document.cookie` is empty for JavaScript;
  - phone width (390 px): no sideways scrolling.
- **Bug found and fixed:** after a deliberate "Sign out", the next person was sent to the previous person's last page. Now the page is remembered only when the session expired or the app opened signed out.

## Not finished / known problems
- **No stubs.** T1 is merged and used for real.
- The case has only user ids, so the manager and HR see ids, not names. There is no "list my cases" route, so the app opens a fixed demo case after sign-in (`firstCaseFor` in `src/demoAccounts.ts`). Both are asked of Maruf on the team board.
- Read-only: confirm and dismiss come with T6, after the interview route (T5).
- `src/demoAccounts.ts` copies the seeded accounts from `backend/app/seed.py`; keep them in step.
- The Plus Jakarta Sans font is not shipped; the app falls back to Segoe UI.
- For Nazha's Selenium flows: `data-testid` hooks are on the demo buttons, the sign-in button and error, the case page, each duty, the error panels and sign-out.

## AI assistance
Claude Code (AI coding assistant) helped read the project files, set up the backend locally, write the frontend, run the checks and the browser test, and write these docs. Choices that were mine: TypeScript over plain JavaScript, and the plan. I review the code before it is pushed. The Congress build was not used; nothing was copied from it.

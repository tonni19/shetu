# Shetu frontend (React + Vite + TypeScript)

The screens of Shetu. Owner: Tonni (board row T2). How it works, file by file: [`docs/CODE-EXPLANATION.md`](../docs/CODE-EXPLANATION.md), section "Frontend skeleton".

## Run it

You need **Node.js 22.22 or newer** (`node --version`), and the backend running first.

1. Start the backend: follow [`backend/README.md`](../backend/README.md). It must answer at http://127.0.0.1:8000/healthz.
2. In a second terminal, from the `frontend/` folder:

```bash
npm install        # once, and again whenever package.json changes
npm run dev        # http://localhost:5173
```

3. Open http://localhost:5173 and click a demo account (all synthetic, password `shetu-demo`).

| Demo account | What you should see |
|---|---|
| Nusrat Jahan (employee) | Their own case in the list; case-1 has two duties |
| Shirin Akter (manager) | Both cases they manage, with the employees' names |
| Farhana Islam (HR) | Every case |
| Tania Akter (cover colleague) | An empty list; typing `/cases/case-1` gives "You cannot open this case" (403) |

## Checks

```bash
npm run typecheck  # TypeScript checks every file against the API shapes
npm run build      # typecheck, then build the release files into dist/ (git-ignored)
```

There is no automated frontend test tool yet: adding one (Vitest is proposed) needs the team's agreement in an Issue (`AGENTS.md`, "Stack"). Until then, the manual checks are listed in the worklog for T2, and the end-to-end flows will be covered by Selenium (Nazha).

## How the app reaches the backend

`vite.config.ts` has a **proxy**: the browser only talks to `localhost:5173`, and Vite forwards `/api/...` and `/healthz` to the backend on port 8000. To the browser it is one site, so the session cookie from sign-in is kept and sent automatically. This is the setting `backend/README.md` asks for. Never call `http://127.0.0.1:8000` directly from the app.

## The libraries, and why each one

Exact versions are pinned in `package.json` (each at least two weeks old when chosen), and `package-lock.json` pins everything below them, so every laptop installs the same thing.

| Library | Why |
|---|---|
| `react`, `react-dom` | The agreed UI library (`AGENTS.md`, "Stack") |
| `react-router` | Page addresses (`/sign-in`, `/cases/case-1`). Version 8 has **no** `react-router-dom`: import from `react-router` |
| `vite`, `@vitejs/plugin-react` | Development server with the proxy, and the release build |
| `typescript`, `@types/react`, `@types/react-dom` | Type checking against the shapes in `docs/API-CONTRACT.md` (see `src/api/types.ts`) |

Do not add a library without the team agreeing in an Issue. Not used, on purpose: Redux, Next.js, CSS frameworks.

## Folder map

```
index.html              the one HTML page; React draws inside <div id="root">
vite.config.ts          dev server, proxy to the backend
tsconfig.json           TypeScript checker settings (strict)
public/shetu-mark.svg   the bridge mark, used as the browser tab icon
src/
  main.tsx              starts React with the router and the session
  App.tsx               the routes and the sign-in guard
  session.tsx           who is signed in (asks GET /api/me at start-up)
  api/types.ts          the contract's shapes as TypeScript types
  api/client.ts         the only place that calls fetch; one ApiError for every failure
  pages/SignInPage.tsx  sign-in form and demo accounts
  pages/CaseListPage.tsx  the cases this person may read (GET /api/cases)
  pages/CasePage.tsx    one leave case with its Role Map, and its error screens
  components/           AppShell, DutyCard, StageSteps, StatusPanel, BridgeMark
  demoAccounts.ts       the seeded demo accounts (copy of backend/app/seed.py)
  format.ts             dates and day counts, computed by code
  styles.css            the Shetu look (tokens shared with docs/learn/index.html)
```

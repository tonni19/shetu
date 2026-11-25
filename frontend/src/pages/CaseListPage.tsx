// FILE:        frontend/src/pages/CaseListPage.tsx
// PURPOSE:     The first page after sign-in: the leave cases the signed-in person may read, from
//              GET /api/cases, each linking to its case page.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/api/client.ts (listCases); src/session.tsx; the route in
//              backend/app/routes/cases.py (Maruf, T1, added in PR #29)
// USED BY:     src/App.tsx (route "/", inside SignedInLayout)
// STATUS:      REAL
// DATA:        Shows synthetic names and dates only. No reason for leave exists to show.
// SECURITY:    The server decides which cases are in the list (can_read_case). The page shows
//              exactly what it gets; it never adds or hides cases itself.
// CONTRACT:    docs/API-CONTRACT.md section 2, "List my cases" (CaseSummary rows, no duties).
// AI NOTE:     This lists leave cases, one per absence, not people's work. Do not add sorting by
//              workload, scores or anything that ranks people (AGENTS.md rules 6 and 12).
//              An empty list is normal (a cover colleague today), not an error.

import { useEffect, useState } from "react";
import { Link } from "react-router";

import { ApiError, listCases } from "../api/client";
import type { CaseSummary, Stage, User } from "../api/types";
import { StatusPanel } from "../components/StatusPanel";
import { formatDate, inclusiveDays, plural } from "../format";
import { useSession, useSignedInUser } from "../session";

type Load = { status: "loading" } | { status: "loaded"; cases: CaseSummary[] } | { status: "failed"; error: ApiError };

const STAGE_NAME: Record<Stage, string> = { map: "Map", hold: "Hold", fit: "Fit" };

/** Load the signed-in person's cases and show them, an empty message, or an error panel. */
export function CaseListPage() {
  const user = useSignedInUser();
  const { sessionExpired } = useSession();
  const [load, setLoad] = useState<Load>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoad({ status: "loading" });
    listCases()
      .then((cases) => {
        if (!cancelled) setLoad({ status: "loaded", cases });
      })
      .catch((caught: unknown) => {
        if (cancelled) return;
        const error = caught instanceof ApiError ? caught : new ApiError(0, "unexpected_reply", "Something went wrong while loading your cases.");
        // 401: the session ended; the guard in src/App.tsx shows the sign-in screen.
        if (error.status === 401) sessionExpired();
        else setLoad({ status: "failed", error });
      });
    return () => {
      cancelled = true;
    };
  }, [attempt, sessionExpired]);

  if (load.status === "loading") {
    return <StatusPanel tone="loading" title="Loading your cases…" testId="cases-loading" />;
  }
  if (load.status === "failed") {
    return (
      <StatusPanel
        tone="error"
        title="Your cases could not be loaded"
        testId="cases-error"
        actions={
          <button type="button" className="button button-primary" onClick={() => setAttempt((n) => n + 1)}>
            Try again
          </button>
        }
      >
        <p>{load.error.detail}</p>
      </StatusPanel>
    );
  }

  const { cases } = load;
  return (
    <section className="case-list" aria-labelledby="cases-title" data-testid="case-list">
      <p className="eyebrow">Shetu</p>
      <h1 id="cases-title" className="case-title">
        {user.role === "employee" ? "Your leave case" : "Leave cases"}
      </h1>
      <p className="muted case-list-lede">{listIntro(user, cases.length)}</p>

      {cases.length === 0 ? (
        <p className="empty" data-testid="cases-empty">
          There are no leave cases for you to see. A cover colleague will see the duties they hold here once cover
          plans exist.
        </p>
      ) : (
        <ul className="case-cards">
          {cases.map((summary) => (
            <li key={summary.id}>
              <CaseCard summary={summary} user={user} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

/** One sentence under the title, so each role knows why they see these cases. */
function listIntro(user: User, count: number): string {
  if (count === 0) return "Nothing to show yet.";
  switch (user.role) {
    case "employee":
      return "Open your case to see your Role Map.";
    case "manager":
      return `${plural(count, "case", "cases")} where you are the manager.`;
    case "hr":
      return `${plural(count, "case", "cases")}. HR can read every case.`;
    case "colleague":
      return `${plural(count, "case", "cases")}.`;
  }
}

/** One case as a link card: who is on leave, when, the stage, and who manages it. */
function CaseCard({ summary, user }: { summary: CaseSummary; user: User }) {
  const days = inclusiveDays(summary.leave_start, summary.leave_end);
  const isOwn = summary.employee_id === user.id;
  return (
    <Link to={`/cases/${encodeURIComponent(summary.id)}`} className="case-card" data-testid={`case-card-${summary.id}`}>
      <span className="case-card-top">
        <span className="case-card-name">{isOwn ? "Your leave" : summary.employee_name}</span>
        <span className="stage-chip">{STAGE_NAME[summary.stage]}</span>
      </span>
      <span className="case-card-dates">
        {formatDate(summary.leave_start)} to {formatDate(summary.leave_end)}
        {days !== null && <span className="muted"> · {plural(days, "day", "days")}</span>}
      </span>
      <span className="case-card-meta">
        Manager: {summary.manager_id === user.id ? "you" : summary.manager_name} · <span className="mono">{summary.id}</span>
      </span>
    </Link>
  );
}

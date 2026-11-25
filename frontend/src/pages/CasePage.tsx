// FILE:        frontend/src/pages/CasePage.tsx
// PURPOSE:     The case page: reads one leave case from the real backend (GET /api/cases/{id})
//              and shows its leave dates, its stage and its Role Map (the duties with evidence).
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/api/client.ts (getCase); src/session.tsx (useSignedInUser); the route in
//              backend/app/routes/cases.py (Maruf, T1)
// USED BY:     src/App.tsx (route "/cases/:caseId", inside SignedInLayout)
// STATUS:      REAL. Read-only. The interview and confirm/dismiss come with T6 (Tonni), after the
//              interview route T5 (Maruf) is merged.
// DATA:        Shows synthetic cases only. There is no reason for leave to show, by design
//              (AGENTS.md rule 5): the page shows dates and duties, never why someone is away.
// SECURITY:    Who may read a case is decided by the server (backend/app/security.py,
//              can_read_case). This page only reports the answer: 403 shows "not allowed".
// CONTRACT:    docs/API-CONTRACT.md section 2, "Read a case", and section 1, "Case" and "Duty".
// AI NOTE:     The case has only user ids (employee_id, manager_id), no names: the contract has
//              no name fields. We show "You" when the id is the signed-in user, otherwise the id.
//              Showing names needs a contract change first (AGENTS.md, "Changing a shared
//              interface"); do not invent a field here.

import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";

import { ApiError, getCase } from "../api/client";
import type { Case, User } from "../api/types";
import { DutyCard, EVIDENCE, EvidenceBadge } from "../components/DutyCard";
import { StageSteps } from "../components/StageSteps";
import { StatusPanel } from "../components/StatusPanel";
import { formatDate, inclusiveDays, plural } from "../format";
import { useSession, useSignedInUser } from "../session";

type Load = { status: "loading" } | { status: "loaded"; data: Case } | { status: "failed"; error: ApiError };

/** Read the case named in the URL and draw it, or the matching error panel. */
export function CasePage() {
  const { caseId = "" } = useParams();
  const user = useSignedInUser();
  const { sessionExpired } = useSession();
  const [load, setLoad] = useState<Load>({ status: "loading" });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoad({ status: "loading" });
    getCase(caseId)
      .then((data) => {
        if (!cancelled) setLoad({ status: "loaded", data });
      })
      .catch((caught: unknown) => {
        if (cancelled) return;
        const error =
          caught instanceof ApiError ? caught : new ApiError(0, "unexpected_reply", "Something went wrong while opening the case.");
        // 401: the session ended (expired or signed out in another tab). The route guard in
        // src/App.tsx then shows the sign-in screen and returns here afterwards.
        if (error.status === 401) sessionExpired();
        else setLoad({ status: "failed", error });
      });
    return () => {
      cancelled = true;
    };
  }, [caseId, attempt, sessionExpired]);

  if (load.status === "loading") {
    return <StatusPanel tone="loading" title="Opening the case…" testId="case-loading" />;
  }
  if (load.status === "failed") {
    return <CaseError caseId={caseId} error={load.error} onRetry={() => setAttempt((n) => n + 1)} />;
  }
  return <CaseView data={load.data} user={user} />;
}

/** The error panels for a case that could not be shown. One per contract error code. */
function CaseError({ caseId, error, onRetry }: { caseId: string; error: ApiError; onRetry: () => void }) {
  if (error.code === "forbidden") {
    return (
      <StatusPanel tone="denied" title="You cannot open this case" testId="case-forbidden">
        <p>{error.detail}</p>
        <p className="muted">
          Only the employee, their manager and HR can read a leave case. The server checked this, not the screen.
        </p>
      </StatusPanel>
    );
  }
  if (error.code === "case_not_found") {
    return (
      <StatusPanel
        tone="error"
        title="Case not found"
        testId="case-not-found"
        actions={
          <Link to="/" className="button button-quiet">
            Open my first case
          </Link>
        }
      >
        <p>
          There is no case called <span className="mono">{caseId}</span>.
        </p>
      </StatusPanel>
    );
  }
  return (
    <StatusPanel
      tone="error"
      title="The case could not be opened"
      testId="case-error"
      actions={
        <button type="button" className="button button-primary" onClick={onRetry}>
          Try again
        </button>
      }
    >
      <p>{error.detail}</p>
    </StatusPanel>
  );
}

/** Who a user id is, from the viewer's point of view: "You" for themselves, else the id. */
function personLabel(id: string, viewer: User): string {
  return id === viewer.id ? "You" : id;
}

/** The loaded case: header, leave window, stage and the Role Map. */
function CaseView({ data, user }: { data: Case; user: User }) {
  const days = inclusiveDays(data.leave_start, data.leave_end);
  const isEmployee = user.id === data.employee_id;
  const counts = {
    said: data.duties.filter((d) => d.evidence_type === "said").length,
    documented: data.duties.filter((d) => d.evidence_type === "documented").length,
    suggested: data.duties.filter((d) => d.evidence_type === "suggested").length,
  };

  return (
    <article className="case" data-testid="case-page">
      <header className="case-head">
        <p className="eyebrow">
          Leave case <span className="mono">{data.id}</span>
        </p>
        <h1 className="case-title">{isEmployee ? "Your leave case" : "Leave case"}</h1>
        <dl className="case-facts">
          <div>
            <dt>Leave</dt>
            <dd data-testid="case-leave">
              {formatDate(data.leave_start)} to {formatDate(data.leave_end)}
              {days !== null && <span className="muted"> · {plural(days, "day", "days")}, both ends included</span>}
            </dd>
          </div>
          <div>
            <dt>Employee</dt>
            <dd className={isEmployee ? undefined : "mono"}>{personLabel(data.employee_id, user)}</dd>
          </div>
          <div>
            <dt>Manager</dt>
            <dd className={user.id === data.manager_id ? undefined : "mono"}>{personLabel(data.manager_id, user)}</dd>
          </div>
        </dl>
      </header>

      <StageSteps current={data.stage} />

      <section className="rolemap" aria-labelledby="rolemap-title">
        <div className="rolemap-head">
          <h2 id="rolemap-title">Role Map</h2>
          <p className="muted">
            {plural(data.duties.length, "duty", "duties")}: {counts.said} said, {counts.documented} documented,{" "}
            {counts.suggested} suggested
          </p>
        </div>
        <p className="rolemap-lede">
          Every duty shows why it is on the map. The AI proposes, rules check, people decide.
        </p>

        <ul className="legend" aria-label="What the evidence labels mean">
          {(Object.keys(EVIDENCE) as (keyof typeof EVIDENCE)[]).map((type) => (
            <li key={type}>
              <EvidenceBadge type={type} />
              <span>{EVIDENCE[type].meaning}</span>
            </li>
          ))}
        </ul>

        {data.duties.length === 0 ? (
          <p className="empty" data-testid="duties-empty">
            No duties on the Role Map yet. They appear here after the interview.
          </p>
        ) : (
          <ul className="duties">
            {data.duties.map((duty) => (
              <li key={duty.id}>
                <DutyCard duty={duty} />
              </li>
            ))}
          </ul>
        )}
      </section>
    </article>
  );
}

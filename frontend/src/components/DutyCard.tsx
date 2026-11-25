// FILE:        frontend/src/components/DutyCard.tsx
// PURPOSE:     Shows one duty of the Role Map with its evidence (why it is on the map) and its
//              confirmation (whether a person has agreed), kept apart on purpose.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/api/types.ts (Duty); src/styles.css (.duty, .badge)
// USED BY:     src/pages/CasePage.tsx. The interview screen (T6) will reuse it and add the
//              confirm and dismiss buttons.
// STATUS:      REAL. Read-only: confirming and dismissing come with T6, once the PATCH route (T5,
//              Maruf) exists.
// DATA:        Shows duty titles, quotes and job description line ids, all synthetic.
// CONTRACT:    docs/API-CONTRACT.md, "Duty": evidence_type and confirmation are separate fields.
// AI NOTE:     Product rules this component shows on screen (AGENTS.md "Rules that must never be
//              broken", rule 1):
//              - "said" shows the employee's exact quote; "documented" shows the job description
//                line; "suggested" is worded as a question, never as a fact (rule R2).
//              - Confirmation is shown on its own line, never merged into the evidence label.
//              - hours_per_week null is shown as "Unknown", never as 0 (rule 3: only a person
//                fills it in).
//              Do not add scores, rankings or progress bars about a person here (rule 6).

import type { Confirmation, Duty, EvidenceType } from "../api/types";

/** The label and one-line meaning of each evidence type, as the legend and badges show them. */
export const EVIDENCE: Record<EvidenceType, { label: string; meaning: string }> = {
  said: { label: "Said", meaning: "The employee said it. Their exact words are kept as evidence." },
  documented: { label: "Documented", meaning: "It is in the job description. The line is kept as evidence." },
  suggested: { label: "Suggested", meaning: "An AI guess. It stays a question until a person confirms it." },
};

const CONFIRMATION_TEXT: Record<Confirmation, string> = {
  pending: "Waiting for the employee to confirm",
  confirmed: "Confirmed by the employee",
  dismissed: "Dismissed by the employee",
};

/** The evidence label, coloured by type. Used on each card and in the legend. */
export function EvidenceBadge({ type }: { type: EvidenceType }) {
  return <span className={`badge badge-${type}`}>{EVIDENCE[type].label}</span>;
}

/** The evidence itself: the quote, the job description line, or the open question. */
function EvidenceDetail({ duty }: { duty: Duty }) {
  switch (duty.evidence_type) {
    case "said":
      // A "said" duty always has a quote (rule R1 checks it on the server). If it is missing,
      // say so instead of showing the duty as if it were backed by words.
      return duty.quote ? (
        <figure className="evidence evidence-said">
          {/* AI NOTE: no lang attribute: a quote may be English, Bangla script or Banglish, and
              the API does not say which. The font stack in styles.css covers Bangla script. */}
          <blockquote className="quote">{duty.quote}</blockquote>
          <figcaption>The employee's own words</figcaption>
        </figure>
      ) : (
        <p className="evidence evidence-missing">The quote for this duty is missing.</p>
      );
    case "documented":
      return (
        <p className="evidence evidence-documented">
          From the job description,{" "}
          {duty.source_line_id ? <span className="mono">line {duty.source_line_id}</span> : "line not given"}
        </p>
      );
    case "suggested":
      return (
        <p className="evidence evidence-suggested">
          Is this part of the role? The AI suggested it. It does not count until the employee confirms it.
        </p>
      );
  }
}

/** One duty card. `duty` comes straight from GET /api/cases/{id}. */
export function DutyCard({ duty }: { duty: Duty }) {
  const hours = duty.hours_per_week === null ? "Unknown" : `${duty.hours_per_week} hours per week`;

  return (
    <article className={`duty duty-${duty.confirmation}`} data-testid={`duty-${duty.id}`} data-evidence={duty.evidence_type}>
      <header className="duty-head">
        <h3 className="duty-title">{duty.title}</h3>
        <EvidenceBadge type={duty.evidence_type} />
      </header>
      <EvidenceDetail duty={duty} />
      <dl className="duty-facts">
        <div>
          <dt>Confirmation</dt>
          <dd className={`confirmation confirmation-${duty.confirmation}`}>{CONFIRMATION_TEXT[duty.confirmation]}</dd>
        </div>
        <div>
          <dt>Time</dt>
          <dd>{hours}</dd>
        </div>
      </dl>
    </article>
  );
}

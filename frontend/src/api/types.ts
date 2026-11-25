// FILE:        frontend/src/api/types.ts
// PURPOSE:     The JSON shapes the backend sends and accepts, written as TypeScript types, so the
//              checker stops a screen from using a field that does not exist or forgetting a null.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  docs/API-CONTRACT.md sections 1 and 2; backend/app/schemas.py (Maruf, T1)
// USED BY:     src/api/client.ts and every screen and component
// STATUS:      REAL. Written by hand from the contract; the routes behind them are merged (T1).
// DATA:        Shapes only, no data. There is no reason-for-leave field and none may be added
//              (AGENTS.md rule 5).
// CONTRACT:    Every type here mirrors a shape in docs/API-CONTRACT.md. If a field changes there,
//              change it here in the same pull request (AGENTS.md, "Changing a shared interface").
// AI NOTE:     These types are checked at compile time only; the browser does not re-check the
//              JSON at run time. The backend guarantees the shape with Pydantic (response_model).
//              Do not invent fields here: propose them in the contract first.

/** CONTRACT: "Who am I" / "Sign in" response. The four roles that exist in backend/app/schemas.py. */
export type Role = "employee" | "manager" | "hr" | "colleague";

export interface User {
  id: string;
  name: string;
  role: Role;
}

/** CONTRACT: body of POST /api/login. Only seeded synthetic accounts exist (backend/README.md). */
export interface LoginRequest {
  user_id: string;
  password: string;
}

/** CONTRACT: Case.stage. Only "map" is used before the progress presentation. */
export type Stage = "map" | "hold" | "fit";

/**
 * CONTRACT: Duty.evidence_type. Why a duty is on the Role Map:
 * - "said":       the employee said it; `quote` holds their exact words (checked by rule R1).
 * - "documented": it is in the job description; `source_line_id` points at the line.
 * - "suggested":  an AI guess. It is only a question until a person confirms it (rule R2).
 */
export type EvidenceType = "said" | "documented" | "suggested";

/** CONTRACT: Duty.confirmation. Set by a person, and kept separate from the evidence type. */
export type Confirmation = "pending" | "confirmed" | "dismissed";

/** CONTRACT: Duty. */
export interface Duty {
  id: string;
  case_id: string;
  /** Short, in the employee's own words. */
  title: string;
  evidence_type: EvidenceType;
  /** The employee's exact words, or null. Present for "said" duties. */
  quote: string | null;
  /** The numbered job description line (for example "jd-3"), or null. Present for "documented". */
  source_line_id: string | null;
  confirmation: Confirmation;
  /** null means unknown. Only a person fills it in, never the AI (AGENTS.md rule 3). */
  hours_per_week: number | null;
}

/**
 * CONTRACT: one row of "List my cases" (GET /api/cases): the Case fields without the duties.
 * Mirrors CaseSummaryOut in backend/app/schemas.py (Maruf, T1, added in PR #29).
 */
export interface CaseSummary {
  id: string;
  employee_id: string;
  /** Display name from the users table, for example "Nusrat Jahan". Synthetic. */
  employee_name: string;
  manager_id: string;
  manager_name: string;
  /** ISO date "YYYY-MM-DD", inclusive. */
  leave_start: string;
  /** ISO date "YYYY-MM-DD", inclusive. */
  leave_end: string;
  stage: Stage;
}

/** CONTRACT: Case, as GET /api/cases/{case_id} returns it: the summary plus the duties. */
export interface Case extends CaseSummary {
  duties: Duty[];
}

/**
 * CONTRACT: "Error". Every error the backend returns has this shape.
 * Codes the screens handle: not_signed_in (401), invalid_credentials (401), forbidden (403),
 * case_not_found (404), invalid_request (422). A failed rule will be 409.
 */
export interface ErrorBody {
  code: string;
  detail: string;
}

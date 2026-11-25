// FILE:        frontend/src/api/client.ts
// PURPOSE:     The only place in the React app that calls the backend. Every route has one small
//              function here, and every failure becomes one ApiError with the contract's
//              {code, detail}, so each screen shows errors the same way.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/api/types.ts; the backend routes in backend/app/routes/ (Maruf, T1), reached
//              through the Vite proxy in vite.config.ts
// USED BY:     src/session.tsx (sign-in state), src/pages/CaseListPage.tsx, src/pages/CasePage.tsx
// STATUS:      REAL. Calls the real backend; there are no stubs in this file.
// DATA:        Sends only a user id and password at sign-in. Never logs request or response bodies.
// CONTRACT:    docs/API-CONTRACT.md section 2: Sign in, Sign out, Who am I, List my cases,
//              Read a case.
// SECURITY:    The session lives in a cookie the server signs; this code never reads or stores it
//              (no localStorage, no tokens in JavaScript). `credentials: "same-origin"` lets the
//              browser send that cookie to our own address, which the proxy forwards to the API.
// AI NOTE:     Paths are relative ("/api/..."), on purpose: the Vite proxy forwards them. Do not
//              hard-code http://127.0.0.1:8000 here, or the cookie stops working.

import type { Case, CaseSummary, ErrorBody, LoginRequest, User } from "./types";

/**
 * An error from talking to the backend.
 * - `status` is the HTTP status, or 0 when the server could not be reached at all.
 * - `code` is the contract's machine code ("forbidden", "case_not_found", ...), or
 *   "network_error" / "unexpected_reply" for the two failures the server cannot describe.
 * - `detail` is a sentence a person can read; screens may show it as it is.
 */
export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly detail: string;

  constructor(status: number, code: string, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.detail = detail;
  }
}

function isErrorBody(value: unknown): value is ErrorBody {
  return (
    typeof value === "object" &&
    value !== null &&
    typeof (value as Record<string, unknown>).code === "string" &&
    typeof (value as Record<string, unknown>).detail === "string"
  );
}

/**
 * Send one request and return the parsed JSON body.
 * Resolves with the body (or undefined for 204 No Content).
 * Rejects with ApiError on any failure: the server's own {code, detail} when it sent one,
 * "network_error" when the server is not running or not reachable, and "unexpected_reply" when
 * the reply is not the JSON we expect.
 */
async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body !== undefined) headers.set("Content-Type", "application/json");

  let response: Response;
  try {
    response = await fetch(path, { ...init, headers, credentials: "same-origin" });
  } catch {
    throw new ApiError(0, "network_error", "Cannot reach the Shetu server. Check that the backend is running.");
  }

  if (response.status === 204) return undefined as T;

  let body: unknown = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }

  if (!response.ok) {
    if (isErrorBody(body)) throw new ApiError(response.status, body.code, body.detail);
    // AI NOTE: the Vite proxy answers 500 or 502 with no JSON when the backend is down.
    const code = response.status >= 500 ? "network_error" : "unexpected_reply";
    const detail =
      response.status >= 500
        ? "The Shetu server is not answering. Check that the backend is running."
        : `The server sent an unexpected reply (HTTP ${response.status}).`;
    throw new ApiError(response.status, code, detail);
  }
  if (body === null) {
    throw new ApiError(response.status, "unexpected_reply", "The server sent an empty or unreadable reply.");
  }
  return body as T;
}

/** POST /api/login. Resolves with the signed-in user; the server sets the session cookie.
 *  Rejects with ApiError 401 "invalid_credentials" for a wrong user id or password. */
export function login(credentials: LoginRequest): Promise<User> {
  return request<User>("/api/login", { method: "POST", body: JSON.stringify(credentials) });
}

/** POST /api/logout (204). The server forgets the session. Safe to call when signed out. */
export function logout(): Promise<void> {
  return request<void>("/api/logout", { method: "POST" });
}

/** GET /api/me. Resolves with the signed-in user, or rejects with ApiError 401 "not_signed_in". */
export function getMe(): Promise<User> {
  return request<User>("/api/me");
}

/**
 * GET /api/cases. Resolves with the cases the signed-in user may read: the employee's own, the
 * manager's, every case for HR, and an empty list for a cover colleague (not an error).
 * Rejects with ApiError 401 "not_signed_in".
 * SECURITY: the server chooses which cases are in the list (can_read_case); the screen shows it.
 */
export function listCases(): Promise<CaseSummary[]> {
  return request<CaseSummary[]>("/api/cases");
}

/**
 * GET /api/cases/{caseId}. Resolves with the case and its duties.
 * Rejects with ApiError 401 "not_signed_in", 403 "forbidden" (for example a cover colleague),
 * or 404 "case_not_found".
 * SECURITY: the 403 is decided by the server (backend/app/security.py, can_read_case). The
 * screen only reports it; hiding things in the browser is not security (AGENTS.md rule 9).
 */
export function getCase(caseId: string): Promise<Case> {
  return request<Case>(`/api/cases/${encodeURIComponent(caseId)}`);
}

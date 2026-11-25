// FILE:        frontend/src/demoAccounts.ts
// PURPOSE:     The seeded demo accounts offered as one-click buttons on the sign-in screen, so a
//              demo can switch between the employee, the manager, HR and a cover colleague.
//              docs/UPDATE-1-PLAN.md asks for this ("Seeded demo accounts").
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  backend/app/seed.py and backend/README.md, "Demo accounts" (Maruf, T1)
// USED BY:     src/pages/SignInPage.tsx
// STATUS:      REAL for the demo: these accounts exist in the seeded database.
// DATA:        Synthetic only. Nobody here is a real person. The password is the public demo
//              password from backend/app/seed.py; real accounts would never be listed like this.
// AI NOTE:     This is a copy of the seed list. If backend/app/seed.py changes a user id, change it
//              here too, or the button will fail with "invalid_credentials". Clicking a button
//              still goes through the real POST /api/login; nothing is skipped.

import type { Role } from "./api/types";

export const DEMO_PASSWORD = "shetu-demo";

export interface DemoAccount {
  userId: string;
  name: string;
  role: Role;
  /** What this account can see, in words, so the presenter knows what to expect. */
  canSee: string;
}

export const DEMO_ACCOUNTS: readonly DemoAccount[] = [
  { userId: "u-nusrat", name: "Nusrat Jahan", role: "employee", canSee: "Their own leave case, case-1" },
  { userId: "u-sabbir", name: "Sabbir Rahman", role: "employee", canSee: "Their own leave case, case-2" },
  { userId: "u-shirin", name: "Shirin Akter", role: "manager", canSee: "case-1 and case-2, as manager" },
  { userId: "u-farhana", name: "Farhana Islam", role: "hr", canSee: "Every case" },
  { userId: "u-tania", name: "Tania Akter", role: "colleague", canSee: "No case yet: the server answers 403" },
];

/** The words shown for each role. Gender-neutral on purpose (AGENTS.md rule 11). */
export const ROLE_LABEL: Record<Role, string> = {
  employee: "Employee",
  manager: "Manager",
  hr: "HR",
  colleague: "Cover colleague",
};

/**
 * The case each demo account opens after signing in.
 * AI NOTE: there is no "list my cases" route in docs/API-CONTRACT.md yet, so the app cannot ask
 * the server which cases a person has. Until that route exists, the employee opens their own
 * demo case and everyone else opens case-1. This decides only which page opens first; the
 * server still checks access on every read. Do not guess cases for unknown users.
 */
export function firstCaseFor(userId: string): string {
  return userId === "u-sabbir" ? "case-2" : "case-1";
}

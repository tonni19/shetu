// FILE:        frontend/src/session.tsx
// PURPOSE:     Remembers, for the whole app, who is signed in. On start-up it asks the server
//              (GET /api/me), because only the server can read the signed session cookie.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/api/client.ts (login, logout, getMe)
// USED BY:     src/App.tsx (the sign-in guard), src/pages/SignInPage.tsx,
//              src/components/AppShell.tsx, src/pages/CasePage.tsx (the user, and an expired session)
// STATUS:      REAL
// DATA:        Holds only the signed-in user's id, name and role, in memory. Nothing is written to
//              localStorage or sessionStorage.
// SECURITY:    This state only decides which screen to draw. It grants no access: every route on
//              the server checks the session again (AGENTS.md rule 9).
// AI NOTE:     Plain React context is enough here. The agreed stack has no Redux (AGENTS.md,
//              "Stack"); do not add a state library for this.

import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

import { ApiError, getMe, login, logout } from "./api/client";
import type { LoginRequest, User } from "./api/types";

/**
 * The four states the app can be in, so no screen has to guess:
 * - checking:    asking the server who is signed in (only at start-up and after "Try again").
 * - signed-out:  nobody is signed in; show the sign-in screen. `returnAfterSignIn` says whether
 *                to come back to the page the person was on (see AI NOTE below).
 * - signed-in:   `user` is who the server says is signed in.
 * - unreachable: the server did not answer, so we cannot know; show how to fix it.
 *
 * AI NOTE: returnAfterSignIn is false after a deliberate "Sign out". Otherwise the next person
 * on the same computer would be sent to the previous person's last page (found in a browser
 * test on 25 November). It is true when the session expired or the app opened signed out.
 */
export type SessionState =
  | { status: "checking" }
  | { status: "signed-out"; returnAfterSignIn: boolean }
  | { status: "signed-in"; user: User }
  | { status: "unreachable"; detail: string };

interface SessionValue {
  state: SessionState;
  /** Sign in. Resolves with the user; rejects with ApiError (for example invalid_credentials). */
  signIn: (credentials: LoginRequest) => Promise<User>;
  /** Sign out on the server, then show the sign-in screen. Never rejects. */
  signOut: () => Promise<void>;
  /** A later call answered 401: the session expired. Show the sign-in screen. */
  sessionExpired: () => void;
  /** Ask the server again (used by the "Try again" button when it was unreachable). */
  recheck: () => void;
}

const SessionContext = createContext<SessionValue | null>(null);

/** Wraps the app and provides the session to every screen below it. */
export function SessionProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<SessionState>({ status: "checking" });
  const [checkCount, setCheckCount] = useState(0);

  useEffect(() => {
    // AI NOTE: `cancelled` stops an old answer from overwriting a newer state, for example
    // when React's development mode runs this effect twice.
    let cancelled = false;
    setState({ status: "checking" });
    getMe()
      .then((user) => {
        if (!cancelled) setState({ status: "signed-in", user });
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        if (error instanceof ApiError && error.status === 401) {
          setState({ status: "signed-out", returnAfterSignIn: true });
        } else {
          const detail = error instanceof ApiError ? error.detail : "Something went wrong while starting Shetu.";
          setState({ status: "unreachable", detail });
        }
      });
    return () => {
      cancelled = true;
    };
  }, [checkCount]);

  const signIn = useCallback(async (credentials: LoginRequest) => {
    const user = await login(credentials);
    setState({ status: "signed-in", user });
    return user;
  }, []);

  const signOut = useCallback(async () => {
    try {
      await logout();
    } catch {
      // Even if the server could not be told, the screen must stop showing the old user.
    }
    setState({ status: "signed-out", returnAfterSignIn: false });
  }, []);

  const sessionExpired = useCallback(() => setState({ status: "signed-out", returnAfterSignIn: true }), []);
  const recheck = useCallback(() => setCheckCount((n) => n + 1), []);

  const value = useMemo(
    () => ({ state, signIn, signOut, sessionExpired, recheck }),
    [state, signIn, signOut, sessionExpired, recheck],
  );
  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

/** Read the session in a component. Throws if used outside <SessionProvider>, which is a bug. */
export function useSession(): SessionValue {
  const value = useContext(SessionContext);
  if (value === null) throw new Error("useSession must be used inside <SessionProvider>.");
  return value;
}

/**
 * The signed-in user, for pages that only exist behind the sign-in guard (SignedInLayout in
 * src/App.tsx). Throws if nobody is signed in, which would mean a page was put outside the
 * guard: a bug to fix in App.tsx, not something to handle on the page.
 */
export function useSignedInUser(): User {
  const { state } = useSession();
  if (state.status !== "signed-in") throw new Error("useSignedInUser is only for pages inside SignedInLayout.");
  return state.user;
}

// FILE:        frontend/src/pages/SignInPage.tsx
// PURPOSE:     The sign-in screen: a user id and password form, and one-click buttons for the
//              seeded demo accounts. Both go through the real POST /api/login.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/session.tsx (signIn), src/demoAccounts.ts, src/api/client.ts (ApiError)
// USED BY:     src/App.tsx (route "/sign-in")
// STATUS:      REAL. Signs in against the backend (Maruf, T1); there is no sign-up.
// DATA:        Synthetic demo accounts only. The password is never stored or logged by the app.
// SECURITY:    A wrong user id and a wrong password give the same message, because the server
//              gives the same error for both (so nobody can find out which accounts exist).
// AI NOTE:     After signing in, the app returns to the page the person first asked for
//              (location.state.from, set by SignedInLayout in src/App.tsx), or else opens their
//              case list (GET /api/cases).

import { useState, type FormEvent } from "react";
import { Navigate, useLocation, useNavigate } from "react-router";

import { ApiError } from "../api/client";
import type { LoginRequest } from "../api/types";
import { BridgeMark } from "../components/BridgeMark";
import { DEMO_ACCOUNTS, DEMO_PASSWORD, ROLE_LABEL } from "../demoAccounts";
import { useSession } from "../session";

/** Where to go after signing in: back to the page that sent us here, or the case list ("/"). */
function destination(state: unknown): string {
  const from = (state as { from?: unknown } | null)?.from;
  // SECURITY: only paths inside this app ("/..."), never "//other-site" or a full URL.
  return typeof from === "string" && from.startsWith("/") && !from.startsWith("//") && from !== "/sign-in" ? from : "/";
}

/** The sign-in screen. Shows an error under the form if sign-in fails; never throws. */
export function SignInPage() {
  const { state, signIn } = useSession();
  const location = useLocation();
  const navigate = useNavigate();

  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  // Already signed in (for example after pressing Back): go straight on.
  if (state.status === "signed-in") {
    return <Navigate to={destination(location.state)} replace />;
  }

  async function attempt(credentials: LoginRequest) {
    setBusy(true);
    setError(null);
    try {
      await signIn(credentials);
      navigate(destination(location.state), { replace: true });
    } catch (caught: unknown) {
      setError(caught instanceof ApiError ? caught.detail : "Sign-in failed. Please try again.");
      setBusy(false);
    }
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (userId.trim() === "" || password === "") {
      setError("Enter a user id and a password.");
      return;
    }
    void attempt({ user_id: userId.trim(), password });
  }

  return (
    <main className="signin" id="main">
      <section className="signin-card" aria-labelledby="signin-title">
        <div className="signin-brand">
          <BridgeMark className="signin-mark" cables={14} />
          <p className="eyebrow">Shetu</p>
        </div>
        <h1 id="signin-title" className="signin-title">
          Sign in
        </h1>
        <p className="signin-lede">Keep a role intact through a planned leave.</p>

        {state.status === "unreachable" && (
          <p className="notice notice-warn" role="alert">
            {state.detail}
          </p>
        )}

        <form className="form" onSubmit={onSubmit} noValidate>
          <label className="field">
            <span className="field-label">User id</span>
            <input
              id="user-id"
              name="user_id"
              autoComplete="username"
              autoCapitalize="none"
              spellCheck={false}
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              disabled={busy}
            />
          </label>
          <label className="field">
            <span className="field-label">Password</span>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={busy}
            />
          </label>
          {error !== null && (
            <p className="form-error" role="alert" data-testid="sign-in-error">
              {error}
            </p>
          )}
          <button type="submit" className="button button-primary" disabled={busy} data-testid="sign-in-submit">
            {busy ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <section className="demo" aria-labelledby="demo-title">
          <h2 id="demo-title" className="demo-title">
            Demo accounts
          </h2>
          <p className="demo-note">
            Synthetic people for the demo. Password <span className="mono">{DEMO_PASSWORD}</span>.
          </p>
          <ul className="demo-list">
            {DEMO_ACCOUNTS.map((account) => (
              <li key={account.userId}>
                <button
                  type="button"
                  className="demo-account"
                  disabled={busy}
                  data-testid={`demo-${account.userId}`}
                  onClick={() => {
                    setUserId(account.userId);
                    setPassword(DEMO_PASSWORD);
                    void attempt({ user_id: account.userId, password: DEMO_PASSWORD });
                  }}
                >
                  <span className="demo-name">{account.name}</span>
                  <span className="demo-role">{ROLE_LABEL[account.role]}</span>
                  <span className="demo-sees">{account.canSee}</span>
                </button>
              </li>
            ))}
          </ul>
        </section>
      </section>
    </main>
  );
}

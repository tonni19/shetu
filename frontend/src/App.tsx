// FILE:        frontend/src/App.tsx
// PURPOSE:     The map of the app's pages (routes), and the guard that sends a signed-out person
//              to the sign-in screen and brings them back afterwards.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  react-router (declarative mode); src/session.tsx; the pages (sign-in, case list,
//              case) and AppShell
// USED BY:     src/main.tsx
// STATUS:      REAL
// DATA:        No data lives here.
// SECURITY:    The guard only decides which screen to draw. The server still checks the session
//              and the case permission on every request (AGENTS.md rule 9).
// AI NOTE:     React Router 8 has no `react-router-dom` package any more: import everything from
//              "react-router". Pages:
//                /sign-in          the sign-in screen (anyone)
//                /                 the cases this person may read (GET /api/cases)
//                /cases/:caseId    the case page (signed in; the server decides 403)
//                anything else     "page not found"
//              Every page that needs a signed-in user goes inside <SignedInLayout>. The
//              interview screen (T6) will be added there as cases/:caseId/interview.

import { Link, Navigate, Route, Routes, useLocation } from "react-router";

import { AppShell } from "./components/AppShell";
import { StatusPanel } from "./components/StatusPanel";
import { CaseListPage } from "./pages/CaseListPage";
import { CasePage } from "./pages/CasePage";
import { SignInPage } from "./pages/SignInPage";
import { useSession } from "./session";

/**
 * The guard and frame for every signed-in page. While the app is still asking the server who is
 * signed in, it shows a loading panel; if the server is down, it says so with "Try again"; if
 * nobody is signed in, it goes to /sign-in, and remembers this address in `state.from` unless
 * the person signed out on purpose.
 * Otherwise it draws the AppShell, which draws the page.
 */
function SignedInLayout() {
  const { state, recheck } = useSession();
  const location = useLocation();

  switch (state.status) {
    case "checking":
      return (
        <main className="page page-centered" id="main">
          <StatusPanel tone="loading" title="Starting Shetu…" />
        </main>
      );
    case "unreachable":
      return (
        <main className="page page-centered" id="main">
          <StatusPanel
            tone="error"
            title="Cannot reach the Shetu server"
            testId="server-unreachable"
            actions={
              <button type="button" className="button button-primary" onClick={recheck}>
                Try again
              </button>
            }
          >
            <p>{state.detail}</p>
            <p className="muted">
              Start it from the <span className="mono">backend</span> folder (see backend/README.md), then try again.
            </p>
          </StatusPanel>
        </main>
      );
    case "signed-out":
      // Remember this page only if the person did not sign out on purpose (see session.tsx).
      return <Navigate to="/sign-in" replace state={state.returnAfterSignIn ? { from: location.pathname } : null} />;
    case "signed-in":
      return <AppShell user={state.user} />;
  }
}

/** Shown for an address the app does not know. */
function NotFound() {
  return (
    <main className="page page-centered" id="main">
      <StatusPanel
        tone="error"
        title="Page not found"
        actions={
          <Link to="/" className="button button-quiet">
            Go to my cases
          </Link>
        }
      >
        <p>There is no page at this address.</p>
      </StatusPanel>
    </main>
  );
}

/** The whole app: one route per page. */
export function App() {
  return (
    <Routes>
      <Route path="/sign-in" element={<SignInPage />} />
      <Route element={<SignedInLayout />}>
        <Route index element={<CaseListPage />} />
        <Route path="cases/:caseId" element={<CasePage />} />
      </Route>
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

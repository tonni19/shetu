// FILE:        frontend/src/components/AppShell.tsx
// PURPOSE:     The frame around every signed-in screen: the Shetu name, who is signed in, and a
//              sign-out button. The screen itself is drawn where <Outlet /> is.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/session.tsx (useSession), src/demoAccounts.ts (ROLE_LABEL),
//              src/components/BridgeMark.tsx
// USED BY:     src/App.tsx (SignedInLayout draws it around every signed-in page)
// STATUS:      REAL
// DATA:        Shows the signed-in user's name and role, as the server returned them.
// AI NOTE:     The synthetic-data note in the footer is on purpose: a demo must never look like it
//              shows real people (AGENTS.md rule 7).

import { Link, Outlet } from "react-router";

import type { User } from "../api/types";
import { ROLE_LABEL } from "../demoAccounts";
import { useSession } from "../session";
import { BridgeMark } from "./BridgeMark";

/** Draw the header, the current screen and the footer for the signed-in `user`. */
export function AppShell({ user }: { user: User }) {
  const { signOut } = useSession();

  return (
    <div className="shell">
      <header className="topbar">
        <Link to="/" className="brand" aria-label="Shetu, home">
          <BridgeMark className="brand-mark" />
          <span className="brand-name">Shetu</span>
        </Link>
        <div className="topbar-user">
          <span className="who">
            <span className="who-name" data-testid="signed-in-name">{user.name}</span>
            <span className="who-role">{ROLE_LABEL[user.role]}</span>
          </span>
          <button type="button" className="button button-quiet" onClick={() => void signOut()} data-testid="sign-out">
            Sign out
          </button>
        </div>
      </header>
      <main className="page" id="main">
        <Outlet />
      </main>
      <footer className="footer">Synthetic demo data. Nobody shown here is a real person.</footer>
    </div>
  );
}

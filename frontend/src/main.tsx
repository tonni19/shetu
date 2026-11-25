// FILE:        frontend/src/main.tsx
// PURPOSE:     Starts the React app: puts it inside <div id="root"> of index.html, with the
//              router (page addresses) and the session (who is signed in) around it.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/App.tsx, src/session.tsx, src/styles.css
// USED BY:     index.html (<script type="module" src="/src/main.tsx">)
// STATUS:      REAL
// DATA:        No data lives here.
// AI NOTE:     StrictMode runs effects twice in development on purpose, to find bugs; the
//              `cancelled` flags in session.tsx and CasePage.tsx handle that.

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router";

import { App } from "./App";
import { SessionProvider } from "./session";
import "./styles.css";

const root = document.getElementById("root");
if (root === null) throw new Error('index.html must contain <div id="root">.');

createRoot(root).render(
  <StrictMode>
    <BrowserRouter>
      <SessionProvider>
        <App />
      </SessionProvider>
    </BrowserRouter>
  </StrictMode>,
);

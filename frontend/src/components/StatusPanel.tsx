// FILE:        frontend/src/components/StatusPanel.tsx
// PURPOSE:     One look for every "not the normal screen" moment: loading, not allowed (403),
//              not found (404), server unreachable. Every screen shows these the same way.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/styles.css (.status-panel)
// USED BY:     src/App.tsx, src/pages/CasePage.tsx
// STATUS:      REAL
// DATA:        Shows only the text it is given.
// AI NOTE:     "loading" uses role="status" and the others role="alert", so a screen reader
//              announces an error as soon as it appears. Keep that when you add a new tone.

import type { ReactNode } from "react";

export type StatusTone = "loading" | "error" | "denied";

/**
 * Show a centred panel with a `title`, an optional longer `children` explanation and optional
 * `actions` (buttons or links). `testId` lets the Selenium flows (Nazha, planned) find the panel.
 */
export function StatusPanel({
  tone,
  title,
  children,
  actions,
  testId,
}: {
  tone: StatusTone;
  title: string;
  children?: ReactNode;
  actions?: ReactNode;
  testId?: string;
}) {
  return (
    <section className={`status-panel status-${tone}`} role={tone === "loading" ? "status" : "alert"} data-testid={testId}>
      {tone === "loading" && <span className="spinner" aria-hidden="true" />}
      <h1 className="status-title">{title}</h1>
      {children !== undefined && <div className="status-body">{children}</div>}
      {actions !== undefined && <div className="status-actions">{actions}</div>}
    </section>
  );
}

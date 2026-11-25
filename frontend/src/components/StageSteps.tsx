// FILE:        frontend/src/components/StageSteps.tsx
// PURPOSE:     Shows the three stages of a leave case, MAP, HOLD and FIT, and which one this case
//              is in, so every viewer sees where the case stands in Shetu's workflow.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  src/api/types.ts (Stage)
// USED BY:     src/pages/CasePage.tsx
// STATUS:      REAL. Display only; the stage is set by the server.
// DATA:        No data beyond the stage name.
// CONTRACT:    docs/API-CONTRACT.md, "Case": stage is "map" | "hold" | "fit".
// AI NOTE:     This shows the stage of the case, not anyone's progress or performance. Do not turn
//              it into a percentage or a score (AGENTS.md rules 6 and 12).

import type { Stage } from "../api/types";

const STAGES: readonly { id: Stage; name: string; when: string }[] = [
  { id: "map", name: "Map", when: "Before leave: write down the role" },
  { id: "hold", name: "Hold", when: "During leave: colleagues hold the duties" },
  { id: "fit", name: "Fit", when: "Before return: agree how the employee comes back" },
];

/** A row of three steps with the `current` one marked. Earlier steps are shown as done. */
export function StageSteps({ current }: { current: Stage }) {
  const currentIndex = STAGES.findIndex((s) => s.id === current);
  return (
    <ol className="stages" aria-label="Stage of this leave case">
      {STAGES.map((stage, index) => {
        const state = index < currentIndex ? "done" : index === currentIndex ? "current" : "later";
        return (
          <li key={stage.id} className={`stage stage-${state}`} aria-current={state === "current" ? "step" : undefined}>
            <span className="stage-name">{stage.name}</span>
            <span className="stage-when">{stage.when}</span>
          </li>
        );
      })}
    </ol>
  );
}

// FILE:        frontend/src/components/BridgeMark.tsx
// PURPOSE:     The Shetu bridge mark ("shetu" means bridge): a red arch over a dark deck with pink
//              cables. Drawn from the same formula as the logo in docs/learn/index.html, so the app
//              and the learning guide look like one product.
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  the colour tokens in src/styles.css (--red, --ink, --pink)
// USED BY:     src/components/AppShell.tsx, src/pages/SignInPage.tsx
// STATUS:      REAL
// DATA:        No data.
// AI NOTE:     Decorative only (aria-hidden). The name "Shetu" next to it is the accessible text.
//              public/shetu-mark.svg is the same drawing for the browser tab icon.

const BASE = 62;
const PEAK = -12;

/** The y position of the arch at fraction t (0 to 1) of its width: a quadratic curve. */
function archY(t: number): number {
  return (1 - t) * (1 - t) * BASE + 2 * (1 - t) * t * PEAK + t * t * BASE;
}

/**
 * Draw the mark. `cables` is how many gaps the arch is split into (more cables for a bigger
 * mark); `className` sizes it from CSS.
 */
export function BridgeMark({ cables = 9, className }: { cables?: number; className?: string }) {
  const lines = [];
  for (let i = 1; i < cables; i++) {
    const t = i / cables;
    const x = (10 + 180 * t).toFixed(1);
    lines.push(<line key={i} x1={x} y1={archY(t).toFixed(1)} x2={x} y2={BASE} stroke="var(--pink)" strokeWidth={2.2} />);
  }
  return (
    <svg className={className} viewBox="0 0 200 80" aria-hidden="true" focusable="false">
      {lines}
      <line x1={2} y1={BASE} x2={198} y2={BASE} stroke="var(--ink)" strokeWidth={3.6} strokeLinecap="round" />
      <path d={`M10 ${BASE} Q100 ${PEAK} 190 ${BASE}`} fill="none" stroke="var(--red)" strokeWidth={4.2} strokeLinecap="round" />
      <circle cx={190} cy={BASE} r={5.5} fill="var(--red)" />
    </svg>
  );
}

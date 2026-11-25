// FILE:        frontend/src/format.ts
// PURPOSE:     Turns the API's ISO dates ("2027-01-10") into words people read ("10 January
//              2027"), and counts the days of a leave. Ordinary code: dates are computed by code,
//              never by the AI (AGENTS.md rule 3).
// OWNER:       Tonni (board row T2)
// DEPENDS ON:  nothing (plain functions)
// USED BY:     src/pages/CasePage.tsx
// STATUS:      REAL
// DATA:        No data lives here.
// AI NOTE:     Never use `new Date("2027-01-10")` for display. JavaScript reads that as midnight
//              UTC, and a browser west of UTC would then show 9 January. We read the year, month
//              and day ourselves and do all date maths in UTC, so every laptop shows the same day.

const ISO_DATE = /^(\d{4})-(\d{2})-(\d{2})$/;

/** Parse "YYYY-MM-DD" into a UTC timestamp. Returns null if the text is not a real date. */
function parseIsoDate(iso: string): number | null {
  const match = ISO_DATE.exec(iso);
  if (match === null) return null;
  const [, y, m, d] = match.map(Number) as [number, number, number, number];
  const time = Date.UTC(y, m - 1, d);
  const check = new Date(time);
  // Rejects impossible dates such as 2027-02-30, which Date.UTC would quietly roll over.
  if (check.getUTCFullYear() !== y || check.getUTCMonth() !== m - 1 || check.getUTCDate() !== d) return null;
  return time;
}

const LONG_DATE = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });

/** "2027-01-10" becomes "10 January 2027". Text that is not a valid date is returned unchanged. */
export function formatDate(iso: string): string {
  const time = parseIsoDate(iso);
  return time === null ? iso : LONG_DATE.format(time);
}

const DAY_MS = 24 * 60 * 60 * 1000;

/**
 * Number of calendar days from `startIso` to `endIso`, counting both ends (the contract's
 * ranges are inclusive). 10 January to 10 January is 1 day.
 * Returns null if either date is invalid or the end is before the start, so the screen can
 * leave the count out instead of showing a wrong number.
 */
export function inclusiveDays(startIso: string, endIso: string): number | null {
  const start = parseIsoDate(startIso);
  const end = parseIsoDate(endIso);
  if (start === null || end === null || end < start) return null;
  return Math.round((end - start) / DAY_MS) + 1;
}

/** "1 duty", "2 duties": simple English plurals for counts shown on screen. */
export function plural(count: number, one: string, many: string): string {
  return `${count} ${count === 1 ? one : many}`;
}

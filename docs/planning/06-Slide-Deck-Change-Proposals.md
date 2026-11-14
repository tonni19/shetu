# Slide deck and workbook: change proposals

- Date: 2026-11-14
- Status: **proposals only.** Nothing here has been applied to `05-Shetu-Proposal-Deck.pptx`, its PDF, or the wording in `04-Workbook-Submission-Draft.xlsx`. The team decides which to accept.

The deck was read slide by slide on 14 November 2026, the day before the proposal presentation. It does not need a rewrite: the wording is short, plain and consistent. The items below are the places where an instructor could question a claim, or where two documents disagree.

If a proposal is accepted, change the `.pptx`, export the PDF again, and add a line to `CHANGELOG.md`.

## 1. Deck: worth fixing before presenting

| # | Slide | Now | Proposed | Why |
|---|---|---|---|---|
| 1 | 8, section label | HOW WE KNOW IT WORKS | HOW WE WILL KNOW IT WORKS | The same slide says "No results yet". The label claims something we cannot show |
| 2 | 9, headline | Working AI at every checkpoint. | Working AI at every update. | The first checkpoint is the proposal, which has a plan and a design but no working AI |
| 3 | 2, statistic | About 2,000 women left Bangladesh's banks in six months. | Bangladesh's banks had about 2,000 fewer women after six months. | The news headline shown on the slide says female employees "drop by 2000". That is a net fall in the count, not a count of women who left. Check the wording against the source before presenting |
| 4 | 9, How we work | Each member owns a feature end to end | Each member will own a feature end to end | `docs/PROJECT-STATE.md` says the work division is proposed, not agreed, and roles are not assigned |
| 5 | 5 and 3, duty names | Slide 5 moves the "quarterly report" deadline. Slide 3 lists a "Monthly portfolio report" and a "Quarter-end review", but no quarterly report | Use the same duty name on both slides | Step 3 on slide 5 flags the report as "due earlier than planned", but step 4 only fixes the renewals. Someone may ask what happened to the report |

For item 3, also prepare an answer to "how do you know this is because of maternity leave?". The slide does not say it is, and the presenter should not say it either.

For item 5, if the slides are not changed, the presenter needs a spoken answer: the example shows one repair, and the report would be re-planned the same way.

## 2. Deck: optional polish

| # | Slide | Now | Proposed | Why |
|---|---|---|---|---|
| 6 | 3 and 9 | "No fixed percentages" / "Fixed percentages" | Remove from slide 3, or explain it in one spoken sentence | The audience has not seen any percentages, so the phrase has nothing to refer to |
| 7 | 9 | "Voice input is a planned extra, after HOLD" sits under How we work | Move it under Honest limits | It is about scope, not about how the team works |
| 8 | 3 | FIT before and after return | Use the same wording as the README ("FIT (return)") or as `AGENTS.md` ("before return") | The documents describe the FIT stage's timing in three different ways |
| 9 | 1, subtitle | An AI-native system that keeps a job intact through a long leave. | An AI system that keeps a job intact through a long leave. | "AI-native" is jargon. The shorter line also stops "leave." from wrapping onto a line of its own |

## 3. Workbook: wording proposals

These are for the pitch cells and feature descriptions in `04-Workbook-Submission-Draft.xlsx`. They keep every fact in the current text and add no numbers or new claims. Cell numbers are the ones after the example rows were removed on 14 November 2026.

Slide 6 uses the same USP sentence as cell G3. If the USP changes in one place, change it in the other.

### Row 3

**D3, Idea**

> Shetu keeps a job intact while the person who does it is on long leave, starting with maternity leave. Its AI interviews her in Bangla, English or Banglish, builds a map of her real job with evidence for every duty, and finds the duties nobody listed. It then plans who covers each duty before she leaves, re-plans when things change, and plans how her work comes back to her. AI proposes, rules check, people decide.

Why: the current opening, "an AI-native workforce continuity system", has to be decoded. This one says what Shetu does.

**E3, Elevator Pitch**

> When someone goes on maternity leave, her work has to pass to other people and come back to her later. Today nobody manages that properly. Shetu does. Its AI interviews her in Bangla, English or Banglish, maps the job she really does, and finds the duties nobody listed. It plans who takes each duty and when, re-plans when a colleague becomes unavailable or a deadline moves, and plans her return around the arrangement she needs. AI proposes, rules check, people decide.

Why: shorter sentences, and "Shetu does." marks the turn from the problem to the answer.

**F3, Project Features**

> 1. An AI interview about her job, in Bangla, English or Banglish
> 2. A Role Map she confirms, with evidence behind every duty
> 3. A check of her account against her job description and documents
> 4. Questions about duties she may have missed
> 5. Handover proposals checked against team capacity
> 6. An owner for every duty on every date
> 7. Changes reported in plain words, with AI re-planning
> 8. Return planning: rules find clashes, AI proposes fixes
> 9. Role-based access, HR approvals and a full decision log

Why: each item starts with what the user gets.

**G3, USP**

> Shetu manages the job, not the leave paperwork. It finds work nobody listed, keeps an owner on every duty for every day of the leave, and proposes a new plan when things change. Everything the AI says traces back to her own words or a document, and a person approves it before it counts.

### Feature table

Most descriptions are already clear and should stay as they are. These are the ones worth changing.

| Cell | Feature | Proposed description |
|---|---|---|
| E11 | Adaptive role interview | She describes her work by typing in Bangla, English or Banglish. The AI reads each answer and asks about what is still missing: when, where, and who depends on it |
| E12 | Evidence-backed Role Map | The AI turns her answers into a list of duties with frequency, timing, place and importance, each linked to her exact words. Rules re-check every date, time and number |
| E13 | Confirm and correct | She reviews every duty and can edit or reject it. Her manager sees nothing until she confirms |
| E14 | Document comparison | She pastes her job description or a handover note. The AI matches it against her duties and lists what the document mentions that she did not, and where the two disagree |
| E16 | State return needs | She enters the arrangement she needs: finish time, days from home, travel limits. No reason is asked for or stored |
| E17 | Review return plan | She sees each clash, the agreed fix and the date each duty returns to her, and can ask HR to review |
| E22 | Impact analysis | Rules list every duty the change leaves uncovered or late, and every colleague it pushes over capacity |
| E23 | Revised plan | The AI proposes a repaired plan, rules re-check it, and the manager approves |

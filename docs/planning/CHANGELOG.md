# Changelog

## Final elevator speech: 14 November 2026

| Change | Why |
|---|---|
| The Excel cell E3 now holds the final 63-word elevator speech written by Tonni | The team finalised it the night before the presentation |
| Pitch pack section 2 leads with the final speech and keeps the earlier versions as drafts; the slide table says slide 1 opens with it and slide 3 explains the hourglass | One speech in three places: the workbook, the pack and the speaker notes |
| The notes of slide 1 hold the speech; the notes of slide 3 no longer call it the thirty-second pitch | The speech is said first, before the introduction |
| One line is flagged: "all data stays on the company's own server" | It describes a design option (a local model on the company's own server), not the lab build, which uses a hosted AI with synthetic data |

## Deck wording fixes 1 to 5 applied: 14 November 2026

| Change | Why |
|---|---|
| Slide 8 label is now "How we will know it works" | The slide says there are no results yet |
| Slide 9 headline is now "Working AI at every update" | The first checkpoint is the proposal, which has no working AI |
| Slide 2 statistic now reads "About 2,000 fewer women in Bangladesh's banks after six months"; the learning guide says the same | The source reports a net fall in the count, not women who left. The slide does not claim a cause |
| Slide 9 now says each member "will own" a feature; pitch pack Q&A likewise | Roles are not agreed yet |
| Slide 3 gains a seventh duty, "Quarterly report"; slide 5 shows both repairs (renewals to Imran, quarterly report to Rafiq) | Slide 5 moved the quarterly report, which slide 3 did not list |
| `05-Shetu-Proposal-Deck.pptx` and its PDF rebuilt; `06-Slide-Deck-Change-Proposals.md` marked with what was applied | Items 6 to 9 stay optional |

## Workbook tidied, deck change proposals added: 14 November 2026

| Change | Why |
|---|---|
| `04-Workbook-Submission-Draft.xlsx`: the faculty's example rows (Order Food, Order Transport), the "DRAFT: Shetu feature breakdown" label row and the second header row were removed. The 21 feature rows now sit directly under the faculty's own header, in rows 11 to 31 | Requested by Mohammad Mahadi Hasan before the proposal. This reverses the Revision 2 choice to leave the example in place |
| Workbook cell E3 (Elevator Pitch) shortened from about 85 words to 58. Pack section 2 now holds the new text as the 20-second version and keeps the earlier one | The earlier pitch repeated most of the Idea cell and was long to say. No other wording in the workbook was changed |
| The workbook was edited by hand, not regenerated. If it is regenerated from the faculty workbook, the example rows will come back | No generator script is in this repository |
| `06-Slide-Deck-Change-Proposals.md` added: nine proposed wording changes to the deck, and proposed wording for the workbook's pitch cells and eight feature descriptions. Only the Elevator Pitch is applied | The deck was reviewed the day before the presentation; the team decides what to accept |
| Checklist section J, the README file table and the overview file table updated | To match the workbook's new rows and list the new file |

## Voice input corrected: 12 November 2026

| Change | Why |
|---|---|
| Voice input is now described everywhere as a stretch feature, first in line after HOLD works, not as dropped. Overview, pitch pack Q&A, report assumptions and the plan slide updated; decision 16 added | The report and pitch pack already said stretch, but the overview, the slide and the instructor summary said it was cut. They now agree |
| A cheaper way to build voice is noted: send recorded audio to the same hosted model through the gateway (about 6 to 12 hours, unverified) | The earlier estimate assumed a separate speech model |

## Moved into the team repository: 12 November 2026

| Change | Why |
|---|---|
| This folder now lives at `docs/planning/` in the private team repository `tonni19/shetu`. The `repo-starter/` drafts became the repository's root files (`README.md`, `AGENTS.md`, `CLAUDE.md`, `docs/PROJECT-STATE.md`, `docs/DECISIONS.md`, `docs/worklog/`, the pull request template); `AI-USAGE.md` and `.gitignore` were added | One shared place for the whole team and their AI assistants |
| References to `repo-starter/` updated in the README, AGENTS, overview, report (25.6) and checklist (K28) | The drafts are now live files |

## Sharing preparation: 12 November 2026

| Change | Why |
|---|---|
| `README.md` added: start-here guide, reading order, file guide, status, ground rules | The folder is being shared with the team |
| `AGENTS.md` and `CLAUDE.md` added at the folder root | So any teammate's AI assistant opening this folder knows what it is and what to read |
| `reference/` added: course documents, competition materials, logos, competition prototype source (no model files or binaries), with its own README | The documents cite these files; teammates do not have the Shetu project on their laptops |
| Paths in the report and pack now point to `reference/` | Same reason |

## Revision 3: 12 November 2026

After the team approved the direction "for now", supplied team details, asked about Flask against Django, and asked for a shared-context system for AI-assisted work.

| Change | Where | Why |
|---|---|---|
| Team name and four members entered | Pack section 0; workbook B3, C3; overview; deck title slide | Provided by the team |
| Stack changed from Flask to **FastAPI plus React**; Django dropped | Report 19.7; pack sections 5 and 6; overview | The instructor advises it; a frontend and backend split suits a four-person team; AI assistance lowers the cost of React. Noted that "Python makes AI easier" applies equally to all three options |
| Scope reductions 1 to 3 now applied from the start | Report 21.4 | The new stack adds roughly 20 to 35 hours to an already tight plan |
| New section 25.6: keeping every teammate's AI assistant in sync | Report | Requested: every session and every push must leave the project state readable by the next person's assistant |
| New folder `repo-starter/` with draft `AGENTS.md`, `CLAUDE.md`, `README.md`, project state, decisions log, worklog guide and pull request template | This folder | Drafts only; nothing was placed in the team repository |
| On-premise position stated | Overview | Hosted AI with synthetic data for the lab; local model for real companies |
| Draft deck built: `05-Shetu-Proposal-Deck.pptx` | This folder | Positioning approved; presentation is on 15 November |
| Slide 8 "How we know it works" added: fake test cases in three language forms, six measures, how the model is chosen, what Shetu will never do. Deck is now 10 slides | Deck; pack 7 | The lab manual asks "how do we know it works?" for every feature, and the main slides never answered it for the AI |
| Appendix removed from the deck: 9 slides, about 6 minutes. Pitch pack section 7 rewritten to match, with a suggested split of slides between four speakers | Deck; pack 7; overview; checklist K29 | Team decision: a class proposal, not a competition |
| Roadmap marked final; overview section 7 rewritten as a step-by-step plan with a setup week; report roadmap aligned with the three simplifications applied from the start | Overview 7; report 22 | Team asked for the final plan |
| Deck redesigned (v2) in the visual system of the team's GP FutureMakers Round 2 deck: crimson, cream and ink colours, Plus Jakarta Sans, the bridge logo, red kicker labels, two-tone headlines. 9 main slides plus 3 appendix slides; PDF copy added | `05-Shetu-Proposal-Deck.pptx`, `.pdf` | The first version was generic and did not match the team's existing brand |
| Checklist rows A1, A2, B1, B2, K7, K9, K13 updated; K28, K29 added | Checklist | Consistency |

Still not done: no model evaluated, no provider chosen, no application code, team repository not accessed.

## Revision 2: 12 November 2026

Made in response to the team's refinement brief, the Hourglass Model request, and the team-collaboration request. Planning documents only. No application code, no repository, and no faculty file was changed. No PPTX was generated.

### Location

The four documents now live in the course folder under `SE-Lab-Investigation/`, as the team asked on 12 November. The refinement brief named the old path inside the Shetu project; the files were updated where they actually are, and no copies were created in the Shetu project.

### 01-Investigation-Report.md

| Change | Why |
|---|---|
| Executive summary rewritten around the confirmed direction and the Revision 2 outcomes | The team confirmed Direction 2 and supplied new decisions |
| New **section 19**: model strategy, verified prices, cost estimate, Colab assessment, local model assessment, gateway design, bake-off protocol, technology stack | Requested. Replaces the old "model choice" paragraph, which had declined to name models |
| New **section 20**: Hourglass Model assessed and adopted as the product's shape through an ownership timeline, without fixed percentages | Requested. Noted that no written record of the six-phase version exists in the project files |
| New **section 21**: four status categories, five scope tiers, effort by module with assumptions, and ordered reductions | Requested. The earlier 220 to 320 hour figure was top-down; the module estimate shows the core MVP alone is 183 to 269 hours |
| New **section 22**: roadmap with Hold-stage re-planning demonstrated by Update 2 and a spike before Update 1 | Requested. Replaces the old iteration table, which left Hold to the fourth iteration |
| New **section 23**: evaluation framework, scenario design, six metrics, reporting templates | Requested. No results are included because none exist |
| New **section 24**: code documentation standards and the module-brief teaching format | Requested |
| New **section 25**: team collaboration: GitHub workflow, unassigned roles, genuine-contribution rules, `CONTRIBUTIONS.md`, Claude's role | Requested |
| New **section 26**: assumptions and decisions still needed | Consolidates what is open |
| Feature matrix: Hold re-planning raised to Must; Ask-the-Handover lowered to next priority; ownership timeline and hourglass view added | Hold intelligence was prioritised by the team; something had to move to keep scope honest |
| Section 12: rows added for model-provider data use, experimental endpoints and evidence traceability | Google's free tier uses submitted data to improve its products, which constrains what may be sent |
| Sections 2, 14, 16, 17, 18 corrected | Presentation date, live sheet, faculty acceptance of prior work, free stack choice, existing repository, placeholders for team details |
| Section 15 elevator pitches revised | To carry the handover, re-planning and return story in one line |

### 02-Requirements-Traceability-Checklist.md

| Change | Why |
|---|---|
| Statuses updated for team name, members, live sheet, pitch length, repository, and cross-references | To match the new facts and section numbers |
| New row B13 for the presentation date | Supplied by the team |
| Section J updated for the regenerated workbook draft | Cell ranges changed |
| New **section K**: 27 team-added requirements with status and location | Keeps team instructions traceable separately from faculty requirements |

### 03-Pitch-Preparation-Pack.md

| Change | Why |
|---|---|
| Rewritten in full | Positioning, scope and structure all changed |
| Section 0: one table for team details, as placeholders | So names are edited in one place; no competition names reused |
| Idea, elevator pitch (three lengths) and USP revised | To include handover, change re-planning and return as one story |
| Feature breakdown rewritten: each row says what the user does and what the AI or the rules do; labelled Prototype or New; limited to the core MVP | Requested; avoids vague entries and over-promising |
| Section 5: one architecture, with the hourglass and the three stages on a single diagram | Requested: one coherent picture, not two frameworks |
| Section 7: five-minute core of seven slides, plus nine optional extension slides | Time limit unknown; estimate is 5 to 10 minutes |
| Team working method and extra faculty questions added | Collaboration requirement |

### 04-Workbook-Submission-Draft.xlsx

| Change | Why |
|---|---|
| Regenerated from the untouched faculty workbook | Preserves the original structure and formatting |
| Row 3: team name and members as placeholders; idea, pitch, features and USP replaced with the revised text | Consistency with the pack |
| Feature table: a header row copied from the faculty's own header style, then 21 rows for the core MVP | Revised breakdown |
| The faculty's example rows 11 to 14 left in place | Not ours to remove |

The original `SE LAB SECTION E PROJECT TEAM.xlsx` was not modified.

### Not done, deliberately

- No model was evaluated and no provider was chosen. The bake-off needs approval, scenarios and a key.
- No evaluation results are stated anywhere.
- No PPTX was built.
- No team names were entered.
- The team's GitHub repository was not accessed.

## Revision 1: 12 November 2026

Initial investigation: report (18 sections), requirements checklist, pitch pack, and workbook draft. Later the same day: clarifications added on the verbal against written AI requirement and the Section C against Section E discrepancy, and the folder moved from the Shetu project to the course folder.

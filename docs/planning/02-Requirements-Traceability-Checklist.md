# Shetu for CSE 3422: Requirements Traceability Checklist

Prepared 12 November 2026; Revision 2 the same day (see `CHANGELOG.md`). One row per requirement found in the course documents. Nothing is marked done unless it exists.

**Status key**

| Status | Meaning |
|---|---|
| Drafted | Content is written in this folder and needs your review |
| Team action | Only the team can do it |
| Not started | Belongs to the build phase; waiting for approval |
| Blocked | Needs information that is not in any document |

**Source key:** CO = Course Outline.pdf; LM1 = Lab Manual.pdf (Class 01); LM2 = Lab Manual 2.pdf (Class 02); PP = Project Pitch Presentation.docx; XL = SE LAB SECTION E PROJECT TEAM.xlsx.

---

## A. Excel workbook (preliminary submission)

The workbook has one visible sheet and no hidden sheets. These are all of its fields.

| ID | Item | Source | Expectation | Deliverable | Status | Where |
|---|---|---|---|---|---|---|
| A1 | Team Name | XL cell B1 | Fill in | Name | Done in the draft: Team Anomaly | Pack, section 0; workbook B3 |
| A2 | Members | XL cell C1 | Fill in | Names and IDs | Done in the draft: four members with IDs | Pack, section 0; workbook C3 |
| A3 | Idea | XL cell D1 | Fill in | Short description | Drafted | Pack, section 1 |
| A4 | Elevator Pitch | XL cell E1 | Fill in; no length given | Short pitch text | Drafted | Pack, section 2 |
| A5 | Project Features | XL cell F1 | Fill in | Feature list | Drafted | Pack, section 4 |
| A6 | USP | XL cell G1 | Fill in | USP statement | Drafted | Pack, section 3 |
| A7 | Feature breakdown format | XL rows 8 to 14 | Module, Sub-module, Features, Description, as in the food and transport example | Table in that shape | Drafted | Pack, section 4 |
| A8 | Check the live sheet | XL (Google Sheets export) | Confirm the shared sheet matches the local copy | Confirmation | Resolved: the team confirms it is the same | |

## B. Pitch presentation

| ID | Item | Source | Expectation | Deliverable | Status | Where |
|---|---|---|---|---|---|---|
| B1 | Slide quality | PP line 1 | Clean and professional | Deck | Draft deck built (`05-Shetu-Proposal-Deck.pptx`); needs team review | Pack, section 7 |
| B2 | Slide tool | PP line 1 | Only Canva or PPTX accepted | Deck in one of those | PPTX | |
| B3 | Display mode | PP line 1 | Present in full-screen mode | Rehearsed delivery | Team action | |
| B4 | Elevator pitch | PP line 2 | "Make ready an elevator pitch" | Spoken pitch | Drafted | Report, section 15 |
| B5 | Defined features | PP line 2 | "Clearly defined features" | Features slide | Drafted | Pack, section 4 |
| B6 | USP | PP line 2 | "A proper USP" | USP slide | Drafted | Pack, section 3 |
| B7 | Attendance | PP line 3 | All team members present | Everyone attends | Team action | |
| B8 | Architecture | PP line 4 | "Clear direction of the project's architecture and breakdown" | Architecture slide and module breakdown | Drafted | Pack, section 5; Report, section 11 |
| B9 | Tech stack | PP line 4 | "Understand the tech stacks you will be using" | Stack slide; every member can explain each choice | Drafted; rehearsal is a team action | Pack, section 6 |
| B10 | Dress code | PP line 5 | Full formal, including formal shoes and a belt | Formal dress | Team action | |
| B11 | Proposal presentation marks | CO, lab 4 | 10% of the course | Delivered pitch | Not started | |
| B12 | Time limit, slide limit | Not stated | Unknown; team estimate 5 to 10 minutes | Five-minute core plus extension slides | Drafted for both lengths | Pack, section 7 |
| B13 | Presentation date | From the team, not in any file | 15 November 2026 | Deck ready before then | Not started; PPTX waits for approval | |

## C. Project rules (from the lab slides)

| ID | Item | Source | Expectation | Deliverable | Status |
|---|---|---|---|---|---|
| C1 | AI at the core | LM1 slide 6 | "Every project must ship AI-enabled, AI-powered features" | Working AI features the product depends on | Not started; design in Report, section 11 |
| C2 | Real problem | LM1 slides 6, 7 | "Solves a real problem well"; problem and users defined | Problem statement | Drafted (Pack, section 1) |
| C3 | User stories | LM1 slide 7 | Each feature written as a user story | Backlog | Not started |
| C4 | Prioritisation | LM1 slide 7 | Must-have against nice-to-have; "cut ruthlessly" | Prioritised list and cut list | Drafted (Report, sections 9 and 21) |
| C5 | Iterations | LM1 slides 7, 21, 22 | Small usable increments; core AI feature first | Iteration plan | Drafted (Report, section 22) |
| C6 | Per-feature answers | LM1 slide 7 | Who is it for, what problem, how do we know it works | Answer per feature | Partly drafted; "how we know" is designed in Report, section 23, and not yet measured |
| C7 | Shared repository | LM1 slides 5, 24 | One shared repo per team; everyone has an account | GitHub repository | Exists, created by a teammate (per the team; not inspected by me) |
| C8 | Commit practice | LM1 slide 5 | Small, frequent commits; history shows who built what | Commit history | Not started; practice defined in Report, section 25 |
| C9 | Branching | LM1 slides 5, 23 | A branch and pull request per feature; issues | PRs and issues | Not started; workflow defined in Report, section 25.1 |
| C10 | Selenium | LM1 slides 5, 7 | Key user flows scripted; run before every demo and merge | Test suite | Not started; flows listed in Report, section 13 |
| C11 | Understand the code | LM1 slide 4 | Understand every line; explain and modify live | Team readiness | Team action |
| C12 | Verify AI output | LM1 slide 4 | "AI can be confidently wrong" | Review habit | Team action |
| C13 | Disclose AI tools | LM1 slide 4 | Note which tools were used and where | `AI-USAGE.md` | Not started; standard defined in Report, section 24 |
| C14 | Relative sizing | LM1 slides 15, 23 | Size features relatively; re-estimate each iteration | Sized backlog | Not started |
| C15 | Range estimates | LM1 slide 16 | Present estimates as a range | Estimates | Drafted as ranges by module (Report, section 21.3) |
| C16 | Demo early and often | LM1 slide 23 | A usable version every iteration | Working build at each update | Not started |
| C17 | Show real users | LM1 slide 7 | "Show it to real users" | Feedback session | Not started; recommended, not required |
| C18 | Three product ideas | LM1 slide 24 | "Bring [3] product ideas"; number is a placeholder | Possibly already past | Blocked: confirm whether still needed |

## D. Graded checkpoints

| ID | Item | Source | Weight | Deliverable | Status |
|---|---|---|---|---|---|
| D1 | Project Proposal Presentation | CO, lab 4 | 10% | Pitch | Not started |
| D2 | Project Update 1 | CO, lab 7 | Part of 20% | About 30% of the project working | Not started |
| D3 | Project Update 2 | CO, lab 9 | Part of 20% | About 60% working | Not started |
| D4 | Final presentation | CO, lab 11 | 15% | 100%, live | Not started |
| D5 | Project Report | CO, lab 12 | 10% | Written report | Blocked: format unknown |
| D6 | Third update | CO | The outline says "Project 3 Updates" for 20% but lists two updates plus a final | Clarify how the 20% is split | Blocked |

## E. Project Show

| ID | Item | Source | Expectation | Status |
|---|---|---|---|---|
| E1 | Live demo | LM1 slide 8 | "A live, working demo, not slides about a demo" | Not started |
| E2 | AI feature | LM1 slide 8 | What it does and how it works | Not started |
| E3 | GitHub history | LM1 slide 8 | How the team built it | Not started |
| E4 | Selenium | LM1 slide 8 | Tests running green | Not started |
| E5 | Product decisions | LM1 slide 8 | What you built, cut and why | Drafted basis (Report, sections 9 and 21.2) |
| E6 | AI workflow | LM1 slide 4 | Show your AI workflow | Not started |
| E7 | Date | LM1 slide 8 | "To be announced" | Blocked |

## F. Concepts taught that the faculty may probe

Not stated as requirements. All are natural parts of the recommended design.

| ID | Concept | Source | In Shetu |
|---|---|---|---|
| F1 | CRUD | CO lab 2; `crud/` | Cases, duties, team, policies |
| F2 | Role-based access checked on the server | LM2 slide 17 | Four roles |
| F3 | Audit trail | LM2 slides 8, 20 | Decision log |
| F4 | Approval workflow | LM2 slide 8 | Manager and HR approvals |
| F5 | State machine | LM2 slides 14, 30 | Case lifecycle |
| F6 | Privacy and consent | LM2 slide 20 | Report, section 12 |
| F7 | Payments | LM2 slide 32 | None needed: licence invoiced to the employer. Prepare the answer |
| F8 | Software type | LM2 slide 5 | An HR module of the kind found in an ERP |

## G. Items requested in the brief but absent from the course documents

Listed so nobody assumes they are required or prepared.

| Item | Found in documents | Action |
|---|---|---|
| UML diagrams | No | Ask about the report format |
| Use-case model | No | Same |
| Formal functional and non-functional requirement lists | No (user stories are asked for instead) | Same |
| Design patterns | No | Same |
| Elevator pitch length | No | Ask |
| Evaluation criteria for the pitch | No | Ask |
| Hidden worksheets | None exist | None |

## H. Documents that could not be fully verified

| Document | Issue |
|---|---|
| Lab Manual 1 and 2 | Text layers were read for every slide. Images were not separately examined; no slide appeared to carry text only as an image |
| Project Pitch Presentation.docx | Created locally on 12 Nov 2026; it appears to be a transcription. If there is an original announcement, check it against this |
| Excel workbook | A local export of a Google Sheet. The live sheet was not accessible |
| Course Outline | States Section C and "Summer 2026"; its PDF title is "Copy of Software Engineering Lab Outline.docx". "Section E" appears only in the workbook's file name. Section-specific details (day, room, dates) should not be relied on; see Report, section 2.6 |

## I. Written against verbal AI requirement

| Bar | Wording | Verifiable in files | Designed for |
|---|---|---|---|
| Written | "AI at its core"; "even a dedicated chatbot counts" (LM1 slide 6) | Yes | Yes |
| Verbal | "AI-native": AI central, not a chatbot bolt-on | No; from the team's account of class | Yes; this is the bar the design targets |

## J. Workbook submission draft

`04-Workbook-Submission-Draft.xlsx` is a copy of the faculty workbook with these cells filled:

| Cell | Field | Status |
|---|---|---|
| B3 | Team Name | Placeholder; team action |
| C3 | Members | Placeholder; team action |
| D3 | Idea | Revised (68 words) |
| E3 | Elevator Pitch | Revised (30-second version, 81 words) |
| F3 | Project Features | Revised (nine-item list) |
| G3 | USP | Revised |
| B11 to E31 | Module, Sub-module, Features, Description | 21 core-MVP feature rows under 5 modules, directly below the faculty's own header (rows 8 to 10). Each description states what the user does and what the AI or the rules do. On 14 November 2026 the faculty's example rows, the "DRAFT" label row and the second header row were removed, which moved the feature rows up from B18 to E38 |

Row 3 and the placement directly under the faculty's header are assumptions about where a team's entry goes; match the live sheet's layout when pasting.

The draft was first generated from the untouched faculty workbook and the text in the pack. The 14 November change was made by hand in the workbook, so regenerating it would bring the example rows back.

## K. Requirements added by the team in Revision 2

These come from the team's instructions, not from course documents. Source key: T = team instruction, 12 November 2026.

| ID | Requirement | Source | Deliverable | Status | Where |
|---|---|---|---|---|---|
| K1 | Provider-independent AI architecture | T | Gateway design with adapters | Designed | Report, 19.5 |
| K2 | Compare hosted API, Hugging Face on Colab, and local model | T | Comparison with verified prices and limits | Done from documentation; quality and latency not measured | Report, 19.2 to 19.4 |
| K3 | Estimated API cost for development, testing and demos | T | Cost table with stated assumptions | Done | Report, 19.2 |
| K4 | Verify the "four-hour" Colab limit | T | Finding | Done: no such limit in Google's FAQ; "at most 12 hours", unpublished and variable | Report, 19.3 |
| K5 | Choose the provider by evaluation on the same synthetic set | T | Bake-off | **Not run.** Protocol and empty results table prepared | Report, 19.5 |
| K6 | Synthetic data only on experimental endpoints | T | Rule | Stated as a design requirement | Report, 12 and 19.3 |
| K7 | Team name and members | T | Entered once provided | Done: provided by the team on 12 November and entered | Pack, section 0; workbook B3, C3 |
| K8 | Keep four categories apart: prototype, proposed before, new for lab, completed in lab | T | Labelling | Done; nothing is in "completed" | Report, 21.1; Pack, 4.2 |
| K9 | Stack chosen on merit and explainability | T | Stack recommendation with alternatives | Revised in Revision 3: FastAPI plus React, following the instructor's advice | Report, 19.7 |
| K10 | Meaningful comments, no commented-out code, `CODE-EXPLANATION.md`, `AI-USAGE.md` | T | Standards | Defined; applies when the build starts | Report, 24.1 |
| K11 | Teach every major module while building | T | Module brief template | Defined | Report, 24.2 |
| K12 | Five-minute core and extended presentation | T | Two structures | Drafted | Pack, 7.1 and 7.2 |
| K13 | No final PPTX before approval | T | None | Respected: built only after the team's approval on 12 November | |
| K14 | Keep Direction 2; separate vision, MVP, next, stretch, excluded | T | Tiered scope | Done | Report, 21.2 |
| K15 | Hold-stage change understanding and re-planning by the 60% milestone | T | Roadmap | Planned for Update 2, with a spike before Update 1 | Report, 22 |
| K16 | Reassess effort by module with assumptions | T | Estimate | Done: core MVP 183 to 269 hours against 170 to 225 assumed capacity | Report, 21.3 and 21.4 |
| K17 | AI evaluation framework with six named metrics, three language forms | T | Dataset design and metric definitions | Designed; no results | Report, 23 |
| K18 | Every milestone demonstrates working functionality | T | Roadmap column "Demonstrable" | Done | Report, 22 |
| K19 | Responsible AI and privacy as architectural requirements | T | Requirements with tests | Done; two rows added for model providers and traceability | Report, 12 |
| K20 | Hourglass Model fitted to Map, Hold, Fit; no fixed percentages | T | Assessment and one architecture | Adopted as the shape, via an ownership timeline. No written record of the earlier six-phase version was found | Report, 20; Pack, 5 |
| K21 | GitHub workflow with individual accounts, branches, Issues, PRs, reviews, stable main | T | Workflow | Defined; nothing set up | Report, 25.1 |
| K22 | Preliminary responsibility areas, not assigned | T | Roles A to D | Done, unassigned | Report, 25.2; Pack, 9 |
| K23 | Genuine individual contributions; no artificial commits | T | Rules | Defined | Report, 25.3 |
| K24 | `CONTRIBUTIONS.md` and evidence of contribution | T | Structure | Defined; file not created | Report, 25.4 |
| K25 | Claude as mentor, not author | T | Working agreement | Defined | Report, 25.5 |
| K26 | Changelog | T | `CHANGELOG.md` | Done | This folder |
| K27 | No implementation, no change to the application or the team repository | T | None | Respected | |
| K28 | Shared, always-updated project context so every member's AI assistant knows the state | T, Revision 3 | `AGENTS.md`, project state, per-PR worklog, decisions log, PR template | Done: in the team repository since 12 November | Repository root and `docs/` |
| K29 | Proposal deck | T, Revision 3 | PPTX: ten slides in the Shetu brand, no appendix (team decision: a class proposal, not a competition) | Built; awaiting team review | `05-Shetu-Proposal-Deck.pptx` |

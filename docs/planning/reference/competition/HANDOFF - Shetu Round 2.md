# Shetu: Round 2 handoff (read this first)

Written 16 Oct 2026 for a fresh chat. It replaces earlier plans. The source of truth for the product is the `Final/` folder; this file adds the decisions, fact-checks, deck plan and prototype status from the chat.

---

## 1. Who and what

- **Team:** Team_Anomaly (always with the underscore), United International University (students): Sadia Noman Tonni, Ahmad Maruf Hossain, Mohammad Mahadi Hasan.
- **Competition:** Grameenphone FutureMakers 2026, category Gender Equality & Inclusion. Round 1 passed (form + 2-minute video). Now Round 2, the Concept Pitch.
- **Product:** Shetu (সেতু, "bridge"). Never write "Setu".

## 2. Hard constraints

| Item | Fact |
|---|---|
| Deck | PowerPoint .pptx, 50 MB or less, **max 10 slides + up to 3 appendix pages** |
| Submission | Uploaded through the organisers' portal only |
| Deadline | **Fri 16 Oct 2026, 4:00 PM** (told by the user earlier; confirm it has not changed) |
| Pitch | **Sat 17 Oct 2026, GP House: 8 minutes pitch + 7 minutes Q&A** |
| Machine | Only PowerPoint confirmed; presented from the organisers' machine, so **no live demo**. The prototype appears inside the deck. |
| Fonts | Use safe fonts (Calibri or Arial). Bangla "সেতু" stays inside the logo PNG; fallback Nirmala UI. |

**Judging criteria (7):** 1 Clarity of Presentation, 2 Depth of Problem Understanding, 3 Solution Strength & Differentiation, 4 AI Application & Technical Rationale, 5 Feasibility & Scalability (execution plan, resources, implementation), 6 Impact (societal, environmental, business), 7 Q&A Handling.

**CEO show (13 Oct) guidance:** a prototype that proves the AI part is feasible is valued; no full system or database expected; the AI part must be solid because AI is the competition's main theme. Q&A is scored separately.

## 3. User's working rules and preferences

- Be honest. No invented statistics. Label illustrative or demo data. **Never claim interviews, a pilot employer, an employer conversation, a lawyer review or real-user tests: none exist.**
- Plain, simple language that judges can follow.
- **No decorative emoji anywhere** (slides, docs, UI). Status colours appear as small coloured dots, not 🔴🟡🟢.
- The user wants the **problem to take the largest share** of the pitch so judges feel it.
- Propose, then wait for approval before building the deck. (The user has not yet approved the deck plan in section 7 or said "go" on the prototype.)

## 4. The final concept (from `Final/1. Shetu Product Brief.docx`)

**One line:** Shetu helps companies keep their best women through motherhood. **Tagline: Keep the people you trained.**

B2B software sold to employers (head of HR). Three stages, one shared record, starting when she tells HR about her leave:

1. **Map (before leave):** a 15-minute AI conversation (Bangla or English, chat or voice) turns her real job into a Role Map (every duty, when, where, how critical). It cross-checks against her job description and the role's recurring cycles, flags work that would be dropped during leave, and proposes cover that does not overload the team. Key duties are marked as held in her name.
2. **Hold (during leave):** nobody contacts her; questions go to the cover person; only changes are logged; any permanent change to held duties needs HR approval with a reason she can read; appraisals use the company's fair leave rule; promotion boards are told she is eligible.
3. **Fit (before and after return):** she enters the arrangement she needs (e.g. 5:30 pm finish, Wednesdays from home, no travel for 3 months) without giving reasons. Shetu finds every clash with her job, including ones nobody remembered, proposes fixes within company policy and team capacity, and gets each confirmed by her manager. Open items go to HR before day one. A 45-day check catches plans that slip.

**Four things only Shetu does:** finds what nobody remembers (quarter-end review from the job description); checks the team, not just her (Rafiq would be overloaded, so Tania); lets nothing fall through (found, proposed, confirmed; 45-day check); protects her career through the gap.

**Time asked per leave:** HR about 2 minutes, manager about 45 minutes, mother about 25 minutes before leave and 5 before return.

**Demo story (illustrative, label "demo data"):** Nusrat, senior relationship manager at "Bank Alpha", 6 months' leave from March. Dropped-work alert: trade renewals for clients C, D, E due about 10 April; planned cover Rafiq has never handled them. Hold log: client F moved after a merger, HR approved; promotion board considered her. Fit: she enters home by 5:30, Wednesdays from home, no travel until December. Shetu asks about the quarter-end loan classification review (in her job description, never mentioned); she says it runs to 9 pm. Return Fit Check finds 3 issues: Tuesday 6:00-7:30 pm credit pre-meeting (move to 3 pm), Chattogram client visits (Rafiq near his limit, so Tania), quarter-end review (start 3 days earlier, she signs off by 5 pm). Result: 0 open issues, sent to HR 23 days before return. Day 45: Tuesday meeting drifted back to 6 pm, reopened and fixed.

**Business:** paid 6-month pilot (up to 5 leaves), then annual licence **BDT 3-6 lakh a year** for 1,000-5,000 staff. First market: 61 scheduled banks, so **BDT 1.8-3.7 crore a year**. Four-person team costs about BDT 32 lakh a year. Growth: other long leaves, telecoms/multinationals/IT, HRIS partners (PeopleDesk, PiHR), Shetu Cover (temporary cover from returning women, placement fee), South Asia.

**Pilot targets:** 0 critical duties without an owner; every return reaches day one with 0 open issues; 9 in 10 plans holding at day 45; at least one issue per leave found that neither she nor her manager listed (the key AI metric); under 1 hour manager time and about 2 minutes HR time per leave. Long-term: 12-month retention vs each company's own past record.

**Trust rules:** starts only after she tells HR; never asks why; each person sees only what they need; no scores or predictions ever; key duties locked in her name; she can ask HR to review; works for any long leave; personal details deleted after the 45-day check; contract bans use in hiring.

Other Final docs: `2.Shetu Judge Q&A Prep.docx` (answers by owner A business, B product/AI, C story/impact/trust) and `3.Shetu Team Roadmap and Pitch Deck Plan.docx` (owners, 10-slide plan timed for 10 minutes, demo script).

## 5. Fact-check of the figures (done in chat, 16 Oct)

| Figure | Status | Source |
|---|---|---|
| SSC 2026: girls 66.68% vs boys 57.86% passed | Verified (deck rounds to 66.7 / 57.9) | Prothom Alo, Dhaka Tribune |
| Women's labour force participation 38.4% vs men 80% (LFS 2024) | Verified (38.40 vs 79.96) | BBS LFS 2024 via The Daily Star |
| Banks/FIs lost about 2,000 women staff in H1 2025 (37,649 to 35,782, about 5%) | Verified | Bangladesh Bank gender report via Prothom Alo, TBS |
| 61 scheduled banks, about 213,000 staff, women about 17% | Verified | Same |
| Banks give 6 months' paid maternity leave | Verified | Bangladesh Bank directive (Dhaka Tribune) |
| Banks may not keep women staff after 6 pm | Verified | Bangladesh Bank directive (Prothom Alo) |
| Labour law maternity leave 120 days (60 + 60), Section 46 | Verified | Labour (Amendment) Ordinance Nov 2025, Act 2026 in force 10 Apr 2026 |
| Childcare room where 40+ women work | Verified, it is **Section 94** (not "Article 98") | Labour Act |
| BRAC returnship: about 1,100 applicants for 15 places; motherhood 25.8% top reason for career breaks | Verified (applicant survey, not national) | TBS, BRAC |
| 54% of parents say inadequate childcare is a major barrier | Verified | RAPID / ILO study via Financial Express |
| Women 11.7 hours a day of care and housework vs men 1.6 | Verified | Daily Star (BBS time use) |
| 63 public childcare centres nationwide | Verified | Financial Express |
| TriNet bought Cocoon for $23M (April 2026), 400+ employers | Verified | TriNet press release |
| Personal Data Protection Ordinance 2025 approved 9 Oct 2025 | Verified | Dhaka Tribune |
| GP runs a workplace daycare (Happy Hearts) | Verified | IFC "Tackling Childcare" report |
| **7.9% of senior bank roles held by women** | **Not found.** Bangladesh Bank reported **9.22%** of top positions (Jul-Dec 2022). Use 9.22% (2022) or drop | Daily Star |
| **"GP daycare since 2006"** | **Year not verified, drop the year** | |
| Replacing an employee costs a fifth of salary or more | US estimate (Center for American Progress); label "US study" | |
| **Break-even "8-11 customers"** | **Math does not match:** 32 lakh / 3-6 lakh = **6-11**. Fix or show the assumption | |
| Mom Project raised $36M by 2020; Parentaly details | Not checked | |
| Interview numbers ("[fill in]") | **None exist. Never put on slides.** | |

## 6. Lessons from reference decks (all in `Final/`)

- **Own draft** `Final/Pitch Decks/Shetu GP FutureMakers Pitch.pdf` (10 slides): good base. Calm design (dark teal title, off-white slides), full-sentence headlines, source line on every slide, 3 problem slides, Map/Hold/Fit, demo cards, AI pipeline, "Easier for everyone", plan and business, impact with ask. Team names still placeholders.
- **SYNAPZ** `Final/Pitch Decks/SYNAPZ_Future-Makers_GP.pdf`: **podium at GP FutureMakers last year**. Copy: persona journey ("Meet Lira") with a pain point and number per stage; a reframe ("Most people believe X... but what if we tell you... it's about access"); slide labels that match the judging criteria; real prototype UI on several slides; concrete BDT prices; month-by-month Gantt execution plan; SDG badges on Impact; a Bangla line. Avoid: clutter, cartoons, unsourced impact percentages.
- **Opion** (`Opion Concept Pitch v2.pdf`, last year's 1st runner-up): clean, but left a blank "can't show this yet" tech slide. Never do that.
- **Astek** (`Final/Astek/` screenshots): evidence-dense; big number + footnote per claim; pilot results tables; team page.
- **Chronicle** (`Final/Chronicle/` screenshots): minimal; one bold claim per slide; friction slide; competitor map.
- **Eka Care** (`Final/Pitch Decks/Eka_Care_Deck.pptx`): product on a phone; traction numbers big; crowded.
- **Y Combinator** (Kevin Hale, "How to Design a Better Pitch Deck"; Geoff Ralston, "Guide to Demo Day Pitches"): legible, simple, obvious; one idea per slide; short headlines; large high-contrast type; lead with the clearest sentence; bottom-up market sizing; the close says exactly what to remember plus the ask; practise. YC says raw screenshots are "the worst", so show product screens as enlarged single cards with captions (GP judges still want to see the product).

## 7. Proposed deck (8:00; problem gets the largest share). Awaiting user approval

Every slide gets a small top label naming its criterion.

| # | Label | Headline | Content | Time |
|---|---|---|---|---|
| 1 | | Shetu: keep the people you trained | Logo, tagline, hook "Bangladesh's banks lost about 2,000 women staff in six months", team names | 0:15 |
| 2 | Problem | Bangladesh educates its daughters, then loses them | Leaking pipeline: 66.7% vs 57.9% SSC, 38.4% vs 80% in work, about 2,000 gone from banks, (9.22% top roles, 2022) | 0:45 |
| 3 | Problem | Motherhood is where we lose them | Nusrat timeline (composite case): duty nobody wrote down, clients split and promotion board without her, 7 pm meetings, resigns 4 months later; 25.8%, 1,100 for 15 places, 6 months' paid leave | 1:00 |
| 4 | Problem | People assume she chose to leave. Nobody owned her job. | Outside vs inside a company's control; cost: paid leave, then replacing her | 0:45 |
| 5 | Solution | Shetu maps, holds and fits her job | Map / Hold / Fit; "Shetu proposes, the manager confirms, HR backs anything left open" | 0:40 |
| 6 | AI solution | Found before she's back | Prototype cards (demo data): quarter-end catch, Rafiq overload, 0 open issues | 1:15 |
| 7 | AI solution | AI finds what people forget. Rules check it. People decide. | Pipeline; what is AI, rules, people; real prototype test numbers | 0:50 |
| 8 | Differentiation | What a meeting can't do | 4 things only Shetu does; time per person; Cocoon / Parentaly / BRAC comparison | 0:40 |
| 9 | Feasibility | Ready to pilot, built to scale | BDT 3-6 lakh, 61 banks, break-even (fixed math), 12-month execution strip, resources | 0:50 |
| 10 | Impact | Keep the next Nusrat | Societal, business, one honest environmental line; SDG 5/8/10 badges; pilot targets; ask: GP as first pilot partner; tagline | 0:45 |

Total 7:45. **Appendix:** A1 AI in detail (architecture, models, rules, test results, cost); A2 Trust and privacy (who sees what, no scores, deletion, hiring ban); A3 Sources and what is not done yet (interviews, pilots, legal review) with the plan.

**Fixes the Final docs still need:** the 10-minute plan must become 8 minutes; no live demo; no interview quotes or numbers; "a leading hosted LLM" is not true (no API key), say an open model running offline on our laptop (stronger privacy story), with a hosted or self-hosted model as a production option; team names; presenter split (the Final plan uses 3 presenters A/B/C; earlier the user said one presenter, so confirm).

## 8. Prototype status

**Not yet rebuilt for the final concept.** The existing code in `prototype/` was built for the OLD concept (voice handover, Ask-the-Handover Q&A, return plans, catch-up). The infrastructure is reusable.

**Machine:** Windows 11, RTX 4050 6 GB, 16 GB RAM (often only about 3 GB free), Python 3.14, torch 2.12 cu130, transformers 5.12, faster-whisper, Flask, PowerPoint and Word installed (COM export to PDF works). No API key available.

**Working offline stack:**
- Language model: `prototype/models/Qwen3-4B-Instruct-2507-Q6_K.gguf` served by `prototype/tools/llama/llama-server.exe` (llama.cpp b11617, CUDA 12.4) on port 8081, JSON mode. Client in `prototype/engines/llm.py` (`ask_json`, auto-starts the server).
- Speech: faster-whisper large-v3 (in HF cache), int8_float16 on GPU, language="bn".
- Embeddings: intfloat/multilingual-e5-small.
- **Gotcha:** loading Qwen with transformers + bitsandbytes 4-bit crashes (access violation / MemoryError on low RAM). Use llama.cpp. HF downloads stall with Xet; use `HF_HUB_DISABLE_XET=1`. An unused 8 GB transformers copy of Qwen sits in the HF cache (can be deleted).

**Reusable rule pieces** (in `prototype/engines/handover.py` and `return_plan.py`): Bangla number words to digits (`normalize_numbers`), number grounding check (every number in AI output must appear in her words), `parse_clock` (reads "সন্ধ্যা ৬টায়" / "6 o'clock evening" as 18:00 by rule, not by the model), quote-matching grounding, greedy capacity-aware cover assignment with task splitting. Lesson from testing: the small model got dates and clock times wrong, so times, numbers and clashes must be done by rules; AI does extraction, cross-check questions and fix proposals.

**To build for the final concept (Map / Hold / Fit, Nusrat demo data):**
- Map: conversation text (+ optional voice) and job description in; AI builds Role Map JSON; AI cross-check lists job-description duties not mentioned and asks about them; rule flags duties due during the leave window without cover (dropped-work alert); cover suggested only from colleagues with spare capacity.
- Hold: change log with HR approval (rules, no AI).
- Fit: her needs in; rules engine finds time, place and travel clashes; AI proposes 2-3 fixes per clash; rules re-check each fix against policy and capacity (Rafiq near limit, Tania offered); status found, proposed, confirmed; "0 open issues".
- A results view that renders saved real outputs for clean slide screenshots; a small test set measuring hidden duties found, false alarms and clash accuracy, reported honestly as team-made test data.

Old-concept assets now obsolete: `Shetu Recording Guide.docx`, `prototype/eval/job_cards.json`, `prototype/samples/`, `Shetu Team Briefing - Round 2.docx`, `Shetu - Brief.docx` (friends' explainer; describes the old concept).

## 9. Files

- `Final/1. Shetu Product Brief.docx`, `Final/2.Shetu Judge Q&A Prep.docx`, `Final/3.Shetu Team Roadmap and Pitch Deck Plan.docx`: the final plan (author byline "@Nafis").
- `Final/Pitch Decks/`: own draft PDF, SYNAPZ PDF, Eka Care pptx. `Final/Astek/`, `Final/Chronicle/`: screenshots.
- Root: `Shetu logo@2x.png` (1280x1280, bridge + "Shetu সেতু" + old tagline "A bridge back to work"; the tagline in the PNG is now outdated), `Option 1 The outlier@2x.png` (Team_Anomaly logo: navy 1B1F3B dots, one orange FF6B35 dot), `Opion Concept Pitch v2.pdf`, earlier Final Product Definition docx/pdf versions.
- Brand palette (old brief; the own draft uses dark teal on off-white): paper F6F8FB, navy 0F1F3D, teal 1A9E9A, gold F2A93B, rose D9486F, muted 6B7690, line DEE4EE.

## 10. Open decisions for the user

1. Confirm the deck deadline (4 PM today?).
2. "Go" on rebuilding the prototype for Map / Hold / Fit.
3. Approve the deck plan in section 7, or edit it.
4. Team names and who presents which slides (1 or 3 presenters).
5. Use 9.22% (2022) or drop the senior-roles figure; fix break-even to 6-11 or give the assumption.
6. The logo PNG still says "A bridge back to work"; new tagline is "Keep the people you trained". Use the logo mark only, or make a new PNG?

## 11. Next steps, in order

1. Get answers to section 10 (at least 1 and 2).
2. Rebuild the prototype (about 1.5 hours), run the test set, capture enlarged screens.
3. Build the .pptx with python-pptx (10 slides + 3 appendix), render each slide to an image and check overflow, overlap and fonts; export a PDF backup.
4. Speaker notes timed to 8:00 by presenter; update the Q&A doc where it conflicts with the truth (hosted LLM, interviews, 10 minutes).
5. Rehearsal: three timed run-throughs; Q&A drills by owner.

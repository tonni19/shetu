# Positioning and Strategy: Five Hard Questions

Written 23 November 2026 from five questions Maruf raised after the presentation (the same questions came up at two places we presented). These are **working answers**: the team adopted them to start building (decision 28), and can refine them. Nothing here is built yet. Where a claim needs checking before we say it aloud, it says so.

**One sentence to anchor everything:**
> Shetu is **role-continuity software**. It keeps a job whole while its owner is away, and guards the return. We build it first for maternity leave, the hardest case; the same engine serves any planned leave.

The four words that carry the idea: **role** (not task), **continuity** (nothing dropped, every duty owned every day), **return** (she comes back to the same job), **evidence** (everything traces to her words or a document).

---

## 1. "Why can't I use it? Why only mothers?"

**You can.** Shetu is for any planned absence of about two weeks or more: study leave, paternity leave, planned surgery, Hajj, a sabbatical, a long secondment. Maternity is our **first and hardest case**, not a limit.

Why start with maternity (a *beachhead*: win the sharpest need first, then expand):

| Reason | Why it makes the product better, not narrower |
|---|---|
| It is **known months ahead** | There is time to map the job properly before leave |
| It is **long** | Work really is dropped, and temporary cover really can become permanent |
| It has a **return that matters** | She may return to a smaller job; the return is where careers are lost |
| It is **legally protected and sensitive** | Forces strict design: no reason field, no medical data, a person decides |
| It has a **clear buyer motive** | Keeping skilled women is a retention, fairness and compliance goal for HR |

**If it works for maternity, it works for everything easier.** A paternity or study leave has the same duties, owners, dates and return, with fewer constraints.

**What we do so nobody feels excluded:**
- Wording in the product is gender-neutral ("the employee", "they"; `AGENTS.md` rule 11).
- There is **no field for the reason for leave**, so the product cannot tell maternity from anything else.
- We demonstrate **two cases** through the same code: a maternity case and a study-leave case.
- The tagline: **"Built for maternity, ready for any long leave."**

**Say this out loud:** "Anyone can use it. We lead with maternity because it is the longest planned leave, it is visible months ahead, and the return is where companies lose people. If it handles that, it handles every other planned leave."

---

## 2. "How do we fit a real domain and make it better?"

Pick the first domain with four tests:

1. **Many skilled employees take planned long leave** (so the problem is frequent).
2. **Duties are partly undocumented** (the knowledge is in people's heads, so our interview finds something a form cannot).
3. **Someone must own every duty every day** (missed work has a cost).
4. **There is a buyer** with an HR function and a reason to keep people.

| Domain | Fit | Note |
|---|---|---|
| Banks and financial institutions | **Strong** | Our own statistic comes from banking; deadlines, approvals and client files are exactly the unwritten duties |
| NGOs and development organizations | **Strong** | Donor reporting calendars, one-person relationships, many women in programme roles |
| Telecom, IT and corporate services | Strong | Knowledge work, clear HR, easy to pilot |
| Hospitals, schools | Medium | Rosters and timetables dominate; a different kind of cover |
| Garments and factories | Large need, different shape | See question 4 |

**Recommended wedge:** knowledge-work teams in banks and NGOs. One department, one planned leave, a short pilot.

**How to make it better inside a domain** (not by adding generic features, but by adding domain depth):
- **Duty templates** per domain (a bank has credit committees, regulatory returns, signing authority; an NGO has donor reports).
- **Authority and deadlines**: in a bank, the real risk is *who is allowed to sign or approve* while the owner is away. A rule that checks delegated authority is something no generic planner has.
- **Domain rule packs** (see question 4) on top of the same core.

*Check before quoting:* we believe the Bangladesh Labour Act 2006 gives 16 weeks of maternity leave (8 before, 8 after birth), and government rules differ. Confirm the exact figures before we state them.

---

## 3. "How do we avoid being a generic workload balancer or AI work manager?"

Shetu is a different **kind** of product, and we keep it different on purpose.

| A generic work manager | Shetu |
|---|---|
| Manages **tasks**, every day | Manages a **role through one absence** (a "leave case") |
| Used daily | Used at **three moments**: before, when something changes, at return |
| Knows only what someone typed in | **Finds duties nobody wrote down** by interviewing the person |
| Balances load for efficiency | Guarantees **coverage**: every duty has an owner every day; load is shown only to stop overload |
| Scores productivity | **Never scores or ranks anyone** |
| Forgets who agreed to what | **Evidence and an audit trail**; the employee confirms their own map |
| Ends when the task ends | **Guards the return**: temporary cover must not quietly become permanent |

**Guardrails we enforce** (also in `AGENTS.md`, rule 12):
- **The litmus test:** "Would this feature be at home in a generic task manager?" If yes, we do not build it.
- **Anti-goals:** no task board, no time tracking, no productivity or performance score, no auto-assignment, no dashboard of an individual's output.
- **Vocabulary:** we say *role, handover, cover, return, continuity*. We avoid *productivity, utilization, task assignment*.
- **Success is measured in continuity**, not efficiency: duties dropped (target zero), the share of people who return to the same role, time to hand over.
- **We prove it, not claim it:** compare Shetu against a plain checklist and a general chatbot on the same fake cases (planned).

---

## 4. "How do we make it work outside corporate offices, such as garments?"

Be honest: garments is **harder**, and not just a matter of translating the screens.

| | Corporate (bank, NGO) | Garments |
|---|---|---|
| What is being covered | A **role** with partly hidden duties | An **operation on a line**, by **skill**, within a production target |
| Where knowledge lives | In heads and email | In the skill matrix and the line plan, mostly explicit |
| Who manages | An office manager | A **line supervisor** |
| Capacity | Hours per week | Skill and line output |
| Compliance | Internal policy | Maternity-benefit rules, payment timing, factory law |
| How people use software | Email and laptops | Phone, supervisor-led, Bangla voice |

**The answer is a sector-neutral core plus sector packs.**
- **The core (what we build)** is the same everywhere: a leave case; duties with evidence; an owner for every duty on every date (the coverage rule); a person approves; an audit log; a return guard.
- **A sector pack** changes only these five things:
  1. **Duty vocabulary and templates** (a bank duty versus a sewing operation).
  2. **What a "duty" is covered by** (a person-by-date, or a skill on a line).
  3. **The capacity model** (hours per week, or the skill matrix and line target).
  4. **Compliance rules** (entitlement and payment checks).
  5. **The input channel and language** (laptop forms, or supervisor on a phone with Bangla voice).
- **For the lab** we do not build a garments pack. We keep the core **sector-neutral** so a pack can be added later, and we **sketch** a garments pack on paper to show it is possible:
  - Name things generically: `duty`, not `client task`.
  - Capacity is **optional** (`hours_per_week` may be unknown; already in the contract).
  - Do not assume email or a corporate calendar.
  - Keep voice input as a planned extra (already decided).

**Say this out loud:** "The core does not care whether a duty is a credit review or a sewing operation. It cares that every duty has an owner on every date and that a person approved it. A sector pack changes the vocabulary, the capacity model and the rules. We prove the core now and sketch the garments pack."

---

## 5. "How do we handle the manager's manual entry, and keep the mother at the centre?"

**Principle: the manager is the operator, she is the protagonist, HR is the buyer.**

| Role | Relationship to Shetu |
|---|---|
| **The employee** (first case: a mother) | The person Shetu **protects**. Her interview builds her own map. She confirms it. The return guard protects her job |
| **The manager** | The person who **uses it most**: approves cover, reports changes, answers availability |
| **The organization (HR)** | The **customer**: retention, fairness, an audit trail |

**How the manager avoids manual work.** The manager does not fill in forms. Most data comes from other places:
1. **The employee's interview** creates the Role Map (the manager does not type duties).
2. **The job description** is read in and matched (later, imported from HR records).
3. The manager only does **three small things**: approve a drafted cover plan, report a change in one sentence ("Tania is away three weeks"), and answer one-tap availability questions.
4. The AI **drafts**, the rules **check**, so the manager reviews instead of writing. The manager's screen is an **attention queue** ("these two leaves need a decision"), not a form.
5. We **measure it**: minutes of manager effort per leave case (to be measured on synthetic cases).

**How the mother stays at the centre while the manager is the main user:**
- **The story and the first case are hers.** The deck, the demo and the first synthetic case follow a mother. The manager is how that story gets solved.
- **Her rights are built in:** nothing counts until she confirms it; she sees everything recorded about her job; nothing is sent to her during leave; nothing becomes permanent without her agreement.
- **The structure of the pitch:** the problem is *her career*, the tool is *the manager's*, the outcome is *the company keeps her*. Same as our elevator speech.

**Say this out loud:** "The manager runs the process, and she is the reason it exists. The manager approves; the AI does the typing. The employee confirms her own job and the return guard protects it."

---

## What this changes in the project

- **Plan:** unchanged for Thursday. The sector-neutral naming and optional capacity are already in the contract. The comparison against a checklist and a chatbot, and short interviews with managers and HR, stay planned.
- **Rules for assistants** (`AGENTS.md`): rule 11 (gender-neutral wording) and rule 12 (stay a role-continuity product; the litmus test and the anti-goals).
- **Pitch and Q&A:** use the sentences marked "Say this out loud".
- **Learning guide:** a new lesson, "Five hard questions", summarises this file.
- **Later:** a sector pack on paper (garments), duty templates for banks and NGOs, a delegated-authority rule for banks.

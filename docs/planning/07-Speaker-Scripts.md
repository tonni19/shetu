# Speaker Scripts for the Proposal Presentation

Presentation: 15 November 2026. Speaker split agreed on 14 November 2026 (decision 21).

**How to read this file.** Tonni's three parts (the elevator speech, slide 2 and slide 3) are exactly as she wrote them. Nobody has edited her words. Every other part is a **draft** written with an AI assistant for the speaker to change into their own words. Drafts say "we will build" for anything not built yet, and must stay true to the slides and to `docs/planning/03-Pitch-Preparation-Pack.md`.

An interactive version with a practice timer was made as a private page; this file is the copy that lives in the repository.

| Speaker | Slides |
|---|---|
| Sadia Noman Tonni | 1 to 3 |
| Mohammad Mahadi Hasan | 4 and 5 |
| Ahmad Maruf Hossain | 6 and 7 |
| Nazha Tarannum Roza | 8 to 10 |

## Sadia Noman Tonni: slides 1 to 3

### Slide 1, the elevator speech

*Exactly as Tonni wrote it.*

Companies lose experienced women after maternity leave because nobody plans her job. Shetu is AI software that maps her duties before leave, protects her role during it, and fits the job to her life before she returns. Her manager confirms every change, and all data stays on the company's own server. The company keeps the person it trained, and she keeps her career.

Cue: Next slide: your slide 2, the problem.

### Slide 2, the problem

*Exactly as Tonni wrote it. She wrote: about 50 seconds.*

In Bangladesh, girls now beat boys in school. In SSC 2026, about 67 percent of girls passed, against 58 percent of boys.

But at work, the picture flips. Only 38 percent of women are in the labour force, against 80 percent of men. And in just six months, our banks had about 2,000 fewer women.

Part of the reason is simple: nobody holds the full picture of her job.

Her job description says she manages clients and submits a monthly report. What it doesn't say is that her clients' statements live only in her email, the Tuesday credit meeting runs till 7:30, and the quarter-end review keeps her until 9.

So when she leaves, work gets dropped. When a colleague falls ill or a deadline moves, nobody re-plans. And when she comes back, the job is still full of late meetings and travel that no longer fit her life.

Cue: Next slide: your slide 3, the solution.

### Slide 3, our solution

*Exactly as Tonni wrote it. She wrote: about 45 seconds.*

Shetu fixes this with one map of her job, across the whole leave.

Before she leaves, Shetu maps every duty, including the unwritten ones, and gives each one an owner. While she's away, it holds that plan: every duty has an owner on every date. And before she returns, it agrees her handover and return dates with her, so the job fits her life.

Plans still break. Here, Tania became unavailable mid-leave. Shetu caught it, proposed a fix, and the manager approved it. Nothing was dropped.

That's Shetu. The company keeps the person it trained, and she keeps her career.

Cue: Hand over to Mahadi for slide 4.

## Mohammad Mahadi Hasan: slides 4 and 5

### Slide 4, why ai is essential

*Draft for Mahadi to edit into their own words.*

So why does Shetu need AI? Without it, this would just be a form, and a form only records what people already remember.

Look at what she really says, in Banglish: the Tuesday credit meeting runs from six to seven thirty in the evening. Shetu reads that mix of Bangla and English and turns it into a row in her Role Map, with her own words kept as the evidence. A line in her job description becomes a documented duty. And when the job description mentions a quarter-end review that she never talked about, Shetu does not guess. It asks her, and until she confirms it, it stays a suggestion.

That is why we split the work three ways. The AI understands language and drafts the plans. Rules check the dates, the numbers and everyone's workload. And people decide.

Cue: Next slide: your slide 5, when the plan breaks.

### Slide 5, hold: when things change

*Draft for Mahadi to edit into their own words.*

Now, what happens when the plan breaks.

The manager simply types it. Tania will be unavailable for three weeks, and the quarterly report deadline has moved to April 2. The AI reads that into facts: who, for how long, and the new date. The sentence has no start date, so the AI asks. It does not guess.

Then plain code takes over. It works out the dates, finds the two affected duties, and checks who has room. The AI proposes Rafiq for the renewals, and the rules reject it: Rafiq has two spare hours and the job needs three. Imran takes the renewals instead, Rafiq takes the quarterly report, and both pass.

Then a person decides. The manager approves or changes it. The AI never applies a change by itself. This is our design. We will build it, and show it working by the 60 percent update.

Cue: Hand over to Ahmad for slide 6.

## Ahmad Maruf Hossain: slides 6 and 7

### Slide 6, features and usp

*Draft for Ahmad to edit into their own words.*

Here is what each person can do.

The employee describes her job in an AI interview and confirms her own Role Map. The manager approves handover proposals that are checked against the team's workload, sees who owns every duty on every date, and reports a change in plain words. The cover colleague sees exactly which duties they hold. HR decides exceptions and reads a log of every proposal, rule check and decision.

What makes Shetu different is simple. It works on the job itself, not the leave paperwork. It finds work nobody listed, and every AI statement traces back to her words or a document.

Cue: Next slide: your slide 7, architecture and technology.

### Slide 7, architecture and technology

*Draft for Ahmad to edit into their own words.*

Now, how we will build it. The plan is simple to build and simple to explain.

Two parts talk through one API. The frontend is React: the screens people use. The backend is Python with FastAPI, as our instructor advised, and it holds the login and roles, the case workflow, the rule checks and the AI pipeline. The data lives in SQLite, a single file that is the same on every laptop.

The app never calls an AI model directly. Every request goes through our own gateway, which checks each reply and can switch provider, so we can change the model without rewriting the app. We have not chosen the model yet. We will run the same fake test cases through several and choose by results. A real company could run the same app on a local model on its own server.

We test the rules with pytest and the user flows with Selenium in a real browser, and we all work in one GitHub repository.

Cue: Hand over to Nazha for slide 8.

## Nazha Tarannum Roza: slides 8 to 10

### Slide 8, how we will know it works

*Draft for Nazha to edit into their own words.*

How will we know it works? We will test the AI, not just trust it.

We write fake test cases in Bangla, English and Banglish, with the right answers written before the AI sees them. Then we measure six things: did it find the real duties, did it invent any, is the evidence correct, did it catch the duties we hid on purpose, how often did the rules reject its plans, and does it say it does not know when it should.

We have no results yet, and results on fake data will never be presented as real-world accuracy. We choose the AI model the same way, by running the same test cases through several models.

And there are things Shetu will never do. It never asks why she needs an arrangement, never stores medical or family details, never scores or predicts anything about a person, and never approves a plan on its own.

Cue: Next slide: your slide 9, the plan.

### Slide 9, plan and scope

*Draft for Nazha to edit into their own words.*

Here is our plan, and every update shows working AI. At the proposal we show the plan and the design. By Update 1, at 30 percent, the first stage works: the interview, the Role Map, and a forgotten duty found. By Update 2, at 60 percent, a change typed in plain words is understood and re-planned. By the final, all three stages work, the tests pass, and the AI is measured.

We cut some things on purpose: live integrations, an AI that acts on its own, scoring people, and fixed percentages. Voice input is a planned extra, after Hold works.

We are honest about our limits. All data is synthetic, we have no user research yet, and the AI can be wrong, so every item needs evidence and a person's approval. We work in one GitHub repository, with a reviewed pull request for every feature, and each of us will own a feature end to end.

Cue: Next slide: your slide 10, the close.

### Slide 10, close

*Draft for Nazha to edit into their own words.*

That is Shetu: keep the people you trained. Thank you. We would be happy to take your questions.

Cue: Then take the questions. See the Questions tab.

## Likely questions

The answers follow section 10 of the pitch pack. The name beside each question is only a suggestion of who answers; the team agrees the split together. Nazha takes the questions first.

| Question | Suggested | Answer |
|---|---|---|
| Is this just a chatbot? | Ahmad | No. The conversation is only the input. The product is the Role Map, the gaps it finds, and the plans it proposes and repairs. Take the AI out and it collapses into a form. |
| What happens when the AI is wrong? | Ahmad | Every item needs a matching quote or document, numbers and times are recomputed by rules, and a person confirms. Unsupported items are flagged, not hidden. A wrong reply never reaches the database. |
| Which model do you use? | Ahmad | Not chosen yet. It sits behind our own gateway, so we can swap it. We will run the same fake test cases through several models and choose by results. A local open model can run fully offline. |
| Does all the data really stay on the company's own server? | Ahmad | That is how Shetu is designed for a real company: the AI can run on a local model on the company's own server, so employee data never has to leave. For this lab we use a hosted model with synthetic data only, and we have not claimed otherwise. |
| How do you know it works? | Nazha | Fake scenarios in Bangla, English and Banglish with answer keys written first, scored on six measures. They are team-written data, and we have no results yet. |
| Is the drop in women in banks because of maternity leave? | Tonni | We do not claim that. It is a net fall in the number of women after six months, and the figures do not give a reason. We use it to show the problem, and Shetu fixes the part a company controls: the job. |
| Did you build this before? | Tonni | The concept and a one-case prototype come from the GP FutureMakers competition, as you know. The application proposed here is a new build, and the repository history will show it. |
| What is the hourglass? | Tonni | The shape of a leave: duties narrow as they pass to colleagues, are held by others during leave, and widen again on return. Map, Hold and Fit manage those three parts. No fixed percentages. |
| Is maternity data sensitive? | Nazha | Yes, so we collect almost none: duties, dates and the arrangement she needs. Never the reason, never medical detail. And we use synthetic data only. |
| Does it need payments? | Nazha | No. It would be licensed to an employer and invoiced. The application has no payment flow. |
| What did you cut? | Nazha | Live calendar and email integrations, autonomous agents, and anything that scores people. Voice input is a planned extra for later. In the first version FIT checks time clashes only. |
| Is the scope realistic? | Nazha | We simplified from the start: FIT checks time clashes only, the AI compares against the job description only, and HR gets a simple approval list. The riskiest AI parts come first, so they are tested early. |
| Did you use AI to write code? | Ahmad | Yes, as the course encourages. Where we used it is recorded in the repository, and every member can explain and modify their own modules. |
| Why React and FastAPI? | Ahmad | You recommended it. It lets frontend and backend work in parallel, and FastAPI is Python, so the AI code plugs in directly and Pydantic validates AI output. |
| Who built what? | Nazha | Each member will own a layer and one feature end to end. The commits, pull requests and reviews on GitHub show it. |

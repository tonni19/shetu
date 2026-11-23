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

So why does Shetu need AI? Because without it, this would just be a form. And a form only records what people already remember.

Think about how she really talks. She might describe her week half in Bangla and half in English, the way most of us do. Shetu understands that, and turns it into one row in her Role Map, with her own words kept right beside it as proof. If a duty is written in her job description, it's marked as documented.

And when the job description mentions something she never brought up, like the quarter-end review, Shetu doesn't guess. It asks her. Until she says yes, it's only a question.

So the work is shared three ways. The AI listens and drafts. Rules check the dates, the numbers and everyone's workload. And people make the decision.

Cue: Next slide: your slide 5, when the plan breaks.

### Slide 5, hold: when things change

*Draft for Mahadi to edit into their own words.*

Now, plans break. That's the part nobody plans for.

Say the manager just types it: Tania will be away for three weeks, and the quarterly report is now due on April 2. Shetu reads that, and it notices something is missing: when does Tania's absence start? So it asks. It doesn't guess.

Then ordinary code does the maths: which dates, which duties are affected, who has time. The AI suggests Rafiq for the renewals. The rules say no. Rafiq has two free hours, and the job needs three. So Imran takes the renewals, Rafiq takes the quarterly report, and this time both pass.

And then the manager decides. She can approve it or change it. Shetu never changes anything on its own.

This is how we've designed it. We will build it, and show it working by the 60 percent update.

Cue: Hand over to Maruf for slide 6.

## Ahmad Maruf Hossain: slides 6 and 7

### Slide 6, features and usp

*Draft for Maruf to edit into their own words.*

So what can people actually do with Shetu?

The employee talks through her job with the AI, then checks and confirms her own map. The manager can see who owns every duty on every date, and can type in a change in plain words. Every proposal comes with a workload check, so nobody ends up overloaded. The colleague covering for her sees exactly what is theirs. And HR can read a log of everything: what was proposed, what the rules said, and who decided.

So what makes us different? Most tools deal with the leave paperwork. We work on the job itself. We find the work nobody wrote down. And everything the AI tells you points back to her own words, or to a document.

Cue: Next slide: your slide 7, architecture and technology.

### Slide 7, architecture and technology

*Draft for Maruf to edit into their own words.*

Now, how will we build it? We're keeping it simple on purpose.

There are two parts, and they talk through one API. The screens are in React. Behind them is Python with FastAPI, which our instructor recommended. That's where the login, the rule checks and the AI pipeline live. And everything is saved in SQLite, one file, the same on every laptop.

One choice matters most. The app never talks to an AI model directly. Everything goes through our own gateway, which checks every answer before we use it. So if we want a different model, we change one place, not the whole app. And we haven't picked a model yet. We'll run the same fake cases through a few of them and choose by the results. A real company could even run a local model on its own server.

We'll test the rules with pytest and the screens with Selenium in a real browser, and all four of us work in one GitHub repository. And to be honest with you: this is our plan. It's not something we've already built.

Cue: Hand over to Nazha for slide 8.

## Nazha Tarannum Roza: slides 8 to 10

### Slide 8, how we will know it works

*Draft for Nazha to edit into their own words.*

So how will we know it works? We won't just trust the AI. We'll test it.

We write fake cases in Bangla, English and Banglish, and we write the right answers first, before the AI ever sees them. Then we measure six things. Did it find the real duties? Did it make any up? Is the evidence correct? Did it catch the duties we hid on purpose? How often did the rules reject its plan? And does it say "I don't know" when it should?

We have no results yet. And when we do, we'll be clear about them: they come from fake data, so they are not real-world accuracy. We'll choose the model the same way, by testing.

And there are things Shetu will never do. It never asks why she needs an arrangement. It never stores medical or family details. It never scores or predicts anything about a person. And it never approves a plan on its own.

Cue: Next slide: your slide 9, the plan.

### Slide 9, plan and scope

*Draft for Nazha to edit into their own words.*

Here's our plan, and at every update you'll see working AI.

Today, it's the plan and the design. By Update 1, at 30 percent, the first stage works: the interview, the Role Map, and a forgotten duty found. By Update 2, at 60 percent, you can type a change in plain words, and Shetu understands it and re-plans. And by the final, all three stages work, the tests pass, and the AI is measured.

We've also chosen what to leave out: live integrations, an AI that acts on its own, scoring people, and fixed percentages. Voice input is something we'd love to add once Hold works.

And we're honest about our limits. All our data is fake. We haven't done user research yet. And the AI can be wrong, which is why everything needs evidence and a person's approval. We work in one GitHub repository, every feature goes through a reviewed pull request, and each of us will own a feature from start to finish.

Cue: Next slide: your slide 10, the close.

### Slide 10, close

*Draft for Nazha to edit into their own words.*

That's Shetu: keep the people you trained. Thank you. We'd be happy to take your questions.

Cue: Then take the questions. See the Questions tab.

## Likely questions

The answers follow section 10 of the pitch pack. The name beside each question is only a suggestion of who answers; the team agrees the split together. Nazha takes the questions first.

| Question | Suggested | Answer |
|---|---|---|
| Is this just a chatbot? | Maruf | No. The conversation is only the input. The product is the Role Map, the gaps it finds, and the plans it proposes and repairs. Take the AI out and it collapses into a form. |
| What happens when the AI is wrong? | Maruf | Every item needs a matching quote or document, numbers and times are recomputed by rules, and a person confirms. Unsupported items are flagged, not hidden. A wrong reply never reaches the database. |
| Which model do you use? | Maruf | Not chosen yet. It sits behind our own gateway, so we can swap it. We will run the same fake test cases through several models and choose by results. A local open model can run fully offline. |
| Does all the data really stay on the company's own server? | Maruf | That is how Shetu is designed for a real company: the AI can run on a local model on the company's own server, so employee data never has to leave. For this lab we use a hosted model with synthetic data only, and we have not claimed otherwise. |
| How do you know it works? | Nazha | Fake scenarios in Bangla, English and Banglish with answer keys written first, scored on six measures. They are team-written data, and we have no results yet. |
| Is the drop in women in banks because of maternity leave? | Tonni | We do not claim that. It is a net fall in the number of women after six months, and the figures do not give a reason. We use it to show the problem, and Shetu fixes the part a company controls: the job. |
| Did you build this before? | Tonni | The concept and a one-case prototype come from the GP FutureMakers competition, as you know. The application proposed here is a new build, and the repository history will show it. |
| What is the hourglass? | Tonni | The shape of a leave: duties narrow as they pass to colleagues, are held by others during leave, and widen again on return. Map, Hold and Fit manage those three parts. No fixed percentages. |
| Is maternity data sensitive? | Nazha | Yes, so we collect almost none: duties, dates and the arrangement she needs. Never the reason, never medical detail. And we use synthetic data only. |
| Does it need payments? | Nazha | No. It would be licensed to an employer and invoiced. The application has no payment flow. |
| What did you cut? | Nazha | Live calendar and email integrations, autonomous agents, and anything that scores people. Voice input is a planned extra for later. In the first version FIT checks time clashes only. |
| Is the scope realistic? | Nazha | We simplified from the start: FIT checks time clashes only, the AI compares against the job description only, and HR gets a simple approval list. The riskiest AI parts come first, so they are tested early. |
| Did you use AI to write code? | Maruf | Yes, as the course encourages. Where we used it is recorded in the repository, and every member can explain and modify their own modules. |
| Why React and FastAPI? | Maruf | You recommended it. It lets frontend and backend work in parallel, and FastAPI is Python, so the AI code plugs in directly and Pydantic validates AI output. |
| Who built what? | Nazha | Each member will own a layer and one feature end to end. The commits, pull requests and reviews on GitHub show it. |

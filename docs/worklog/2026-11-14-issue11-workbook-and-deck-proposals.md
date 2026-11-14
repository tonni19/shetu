# Issue #11: Tidy the workbook draft and propose wording changes to the deck

- Prepared by: Mohammad Mahadi Hasan, with an AI assistant
- Branch: `feature/workbook-cleanup-deck-proposals`
- Date: 2026-11-14

## What was done
- In `docs/planning/04-Workbook-Submission-Draft.xlsx`, the faculty's example rows (Order Food, Order Transport), the "DRAFT: Shetu feature breakdown" label row and the second header row were removed. The 21 feature rows now sit directly under the faculty's own header, in rows 11 to 31.
- The Elevator Pitch cell (E3) was shortened from about 85 words to 58. The pitch pack, section 2, holds the new text and keeps the earlier one.
- The 10 proposal slides and the rest of the workbook wording were reviewed. The suggestions are in `docs/planning/06-Slide-Deck-Change-Proposals.md`. They are proposals: the deck and its PDF are unchanged.
- The planning changelog, checklist section J, the planning README and overview file tables, the project state and `AI-USAGE.md` were updated.

## Why
The example rows and the "DRAFT" label should not be in what the team submits. The earlier pitch repeated most of the Idea cell. The deck review found a few claims an instructor could question, and the team needs them in one place to decide before 15 November.

## How it works
Documents only, no code. The workbook was edited directly: rows 11 to 17 were removed from the sheet, the later rows moved up by seven, and the three merged cells that belonged to the example were removed with them.

## How it was tested
The cell contents were read back from the edited workbook: the example and the label are gone, the feature rows start at row 11, the new pitch is in E3, and the sheet's XML is well formed. **The edited workbook has not been opened in Excel**, so its layout and borders still need a visual check.

## Not finished / known problems
- Removing the example reverses an earlier choice recorded in the changelog ("Not ours to remove"). The reviewer should confirm the team agrees.
- The workbook was edited by hand. If it is regenerated from the faculty workbook, the example rows and the earlier pitch will come back.
- The slide proposals are not applied. If any are accepted, the `.pptx` and the PDF need changing, and slide 6 shares its USP sentence with workbook cell G3.
- The statistic on slide 2 was compared only with the headline shown on the slide, not with the original report.
- `docs/PROJECT-STATE.md` still lists Issue 7 as in progress and does not list pull requests #8, #9 and #10 as merged. Not changed here.

## AI assistance
Claude Code made the workbook edits, reviewed the slides, and drafted the pitch, the proposals and the document updates. The member asked for each change and chose which wording to apply. Recorded in `AI-USAGE.md`.

# 2026-11-16: GitHub Pro active, guide online, main protected

## What was done
- `tonni19`'s GitHub Pro is active (checked by the team on 16 November, and confirmed when GitHub accepted the Pages setting on the private repository).
- Turned on GitHub Pages for the repository with GitHub Actions as the source, using `tonni19` (the owner).
- Added `.github/workflows/learn-guide.yml`, which publishes only `docs/learn` to https://tonni19.github.io/shetu/ whenever that folder changes on `main`. It was pushed from `SpicyFalcon619` because `tonni19`'s login does not have the `workflow` permission.
- Branch protection for `main` is turned on before this pull request is merged (decision 23), so this is the first pull request that needs an approving review from another member (Tonni).
- Project state: the proposal is marked done, with the feedback we got (why only mothers, where is the niche, isn't it a work planner; the instructor mentioned tokenization and vectorization), and the next steps are answering that feedback and assigning roles.

## Learning guide: Deeper, in plain words
- Added six lessons, explained to Ahmad first and then written down for the whole team: Rules, exactly; Tests and pytest; The architecture, piece by piece; The AI pipeline; Tokens and embeddings; Our niche. Each has a short quiz (also in the final exam), and nine glossary terms were added. The glossary is now sorted when shown.
- The niche framing and the use of embeddings are marked "Proposed, not agreed" in the guide.
- Fixed a phone layout bug in the whole guide: wide tables or code could make the page scroll sideways.
- Checked in a headless browser at 1280 px and 390 px: every new lesson shows, has its quiz and lesson buttons, no sideways scrolling, no script errors.

## Not finished / known problems
- The niche answer and the use of embeddings are not agreed yet. The role split is discussed on 17 November.
- The Pages site is public. Only `docs/learn` is published; keep personal data out of it.
- No code exists yet.

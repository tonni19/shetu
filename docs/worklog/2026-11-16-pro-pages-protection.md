# 2026-11-16: GitHub Pro active, guide online, main protected

## What was done
- `tonni19`'s GitHub Pro is active (checked by the team on 16 November, and confirmed when GitHub accepted the Pages setting on the private repository).
- Turned on GitHub Pages for the repository with GitHub Actions as the source, using `tonni19` (the owner).
- Added `.github/workflows/learn-guide.yml`, which publishes only `docs/learn` to https://tonni19.github.io/shetu/ whenever that folder changes on `main`. It was pushed from `SpicyFalcon619` because `tonni19`'s login does not have the `workflow` permission.
- Branch protection for `main` is turned on after this pull request is merged (decision 23), so this is the last pull request merged without a recorded review.
- Project state: the proposal is marked done, with the feedback we got (why only mothers, where is the niche, isn't it a work planner; the instructor mentioned tokenization and vectorization), and the next steps are answering that feedback and assigning roles.

## Not finished / known problems
- The niche answer and the role split are not agreed yet.
- The Pages site is public. Only `docs/learn` is published; keep personal data out of it.
- No code exists yet.

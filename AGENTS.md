# sleep-videos — agent rules

- Branch flow: `feature/<name>` → PR into `develop` → PR from `develop` into `main`. Never push directly to `main` or `develop`.
- `main` accepts PRs only from `develop`; `develop` accepts PRs only from `feature/*`. Enforced by rulesets plus the `source-branch` check in `.github/workflows/branch-policy.yml`.
- Copilot code review runs automatically on PRs into `develop` only.
- Media: commit a video only after `scripts/compress_videos.py` has written it from its FLAC master (default 160 kb/s AAC). No tracked file may exceed 1,000,000,000 bytes. `masters/` and `renders/` are never tracked, and nothing under `site/` may be in Git LFS. Enforced by `.github/workflows/media-guard.yml`.
- Replacing a committed full video needs owner sign-off: each replacement permanently adds about 0.6 GB of LFS storage. Clone without videos with `GIT_LFS_SKIP_SMUDGE=1`.
- Feature PRs are squash-merged into `develop`; `develop` → `main` uses merge commits.
- Design context: `PRODUCT.md` and `DESIGN.md` (Impeccable). Designs live in `docs/designs/`.
- EGM artifact directory: docs/designs/review

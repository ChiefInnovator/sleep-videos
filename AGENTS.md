# sleep-videos — agent rules

- Branch flow: `feature/<name>` → PR into `develop` → PR from `develop` into `main`. Never push directly to `main` or `develop`.
- `main` accepts PRs only from `develop`; `develop` accepts PRs only from `feature/*`. Enforced by rulesets plus the `source-branch` check in `.github/workflows/branch-policy.yml`.
- Copilot code review runs automatically on PRs into `develop` only.

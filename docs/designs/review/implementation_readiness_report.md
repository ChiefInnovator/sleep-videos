# Stage 9 — Implementation Readiness Test

Target: `docs/designs/repo-consolidation.md`, DetailedRange 276–440. Reviewers: `egm-implementation-readiness`, `egm-codebase-details` (implementation-readiness-standard), `egm-style`. Duplicate findings are merged.

Note: `egm-codebase-details` had no git access, so it could not read `origin/develop:AGENTS.md` or `branch-policy.yml`. The elephant confirmed both: `develop` = `main` (d7498dd) + commit 7988fc4. They share history with local `main`, so no `--allow-unrelated-histories` is needed.

## 🔴 Blockers

- **R-B1: The branch setup cannot run, and the obvious workaround puts the masters into history.** [readiness, codebase] `git merge` refuses to run with a staged index, and committing first captures the masters, the 320k videos and the zip. **Fix:** exact commands: `git switch -c feature/repo-consolidation`, then `git rm --cached` the masters, videos, preview MP4s and zip; apply `.gitignore`/`.gitattributes`; size-audit the index; commit; `git merge origin/develop`; audit the pushed objects before every push.
- **R-B2: No phases or execution order.** [readiness, codebase] **Fix:** use numbered phases, each with an exit check (index cleanup → script changes → compression → workflows/docs → PR to develop + ruleset update → Pages cutover + PR to main).
- **R-B3: The encoder command is incomplete. It lacks `-t <seconds>`**, which `video_qc`'s `duration <= seconds` assertion needs. The input order and the `aac_at` detection are also unstated. [readiness, codebase] **Fix:** give the full argv, and detect `aac_at` via `ffmpeg -hide_banner -encoders`.
- **R-B4: `media-guard` is prose, not an implementable spec.** [readiness, codebase] **Fix:** put the full YAML and shell in the plan: `git ls-files -s` → `git cat-file blob` → LFS pointer detection and `size` parsing → path→report mapping → `jq`; `runs-on`, permissions, and failure messages that name the file and the rule.

## 🟡 Major

- **R-M1: `video_qc` contract.** It returns a dict and writes the `.rgb-framemd5` sidecar for previews; full runs need `.venv/bin/python` and the built `verify-black-frames`; `probe.format.filename` must be patched to the final path. [readiness, codebase]
- **R-M2: Temp-file naming and ignores.** Use `*.tmp.mp4` (with ignore). `*.uncompressed.mp4` is never produced. The unstaged zip must be ignored or deleted. [readiness, codebase]
- **R-M3: Report schema untyped.** Define the types for `bytes` (int), `bitrate`, and `sha256` (lowercase hex), and the relative paths. [readiness]
- **R-M4: The 650 MB goal is not enforced. The estimate is also low:** rain-on-window projects to about 610–625 MB. Check size before the hours-long QC. [readiness, codebase]
- **R-M5: `pages.yml` is incomplete.** It needs the `environment: github-pages` block with the URL output, pinned action majors, and concurrency settings. Permissions are inconsistent with the NFR. [readiness, codebase]
- **R-M6: Repo-settings changes have no commands.** Specify the exact `gh api` calls for the Pages `build_type`, the rollback, and the ruleset PUTs. Add the required check only after `media-guard.yml` lands on `develop`. [readiness]
- **R-M7: The test plan covers one negative case.** Add tests for: oversized LFS pointer (fake `size`), missing/mismatched report, LFS under `site/`, compressor failure path (no target, temp or report left), `aac_at` fallback, regeneration match, and the published preview's `Content-Length` (not a pointer). [readiness, codebase, style]
- **R-M8: Doc edits have no target text.** The README lines needing changes are 3, 13, 17 and 57; `review.html` lines 10 and 14 plus its cache-buster; `site/README.md` and `AGENTS.md` need their exact paragraphs. [readiness, codebase]
- **R-M9: Stale hash and report evidence.** `reports/full-artifact-hashes.json`, `SHA256SUMS` and `<k>-full.json` describe the 320k `videos/` files. Rekey them or label them as v1.0.0. [codebase]
- **R-M10: The size-audit command is invalid.** Use `git ls-files -s | awk '{print $2}' | git cat-file --batch-check='%(objectname) %(objectsize)'` plus pointer parsing. [codebase, style]
- **R-M11: `<mode>` is undefined, and the 1 GB ceiling is written five ways.** Define 1 GB as 1,000,000,000 bytes. [style]
- **R-M12: The negative guard test closes a PR it never opened; `actionlint` "if available" is optional.** [style]

## 🟢 Nits

Name `produce.py:272` / `verify_deliveries.py:25` exactly. Reuse `verify_deliveries.digest`. `update_title_previews.py` also needs the poster copied to `site/media/`. Add `renders/` to guard rule 1. Remove redundant sentences (312–313, 296–297). Fix informal wording. "At cutover" is undefined. Optional `git lfs prune`.

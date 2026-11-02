# Stage 8 — Intermediate Zoom Out Review

Target: `docs/designs/repo-consolidation.md` (full file), weighed against the Stage 5–7 reports. Reviewer: `egm-zoom-out` (Goldfish).

**Verdict:** A small revision is needed. 1 blocker, 4 major, 3 nits. Several Stage 6–7 mitigations are bigger than the risk they cover.

## Changes to make

- 🔴 **Ordered first-commit checklist (278–281, 299–306).** The only path to permanent LFS loss that cannot be recovered is committing or pushing while the masters are still staged. **Fix:** use numbered steps. Unstage the masters, videos, preview MP4s and the zip, and apply the ignore/attributes changes. Then run `git lfs ls-files -s`, and push only if nothing is under `masters/` and nothing is over 1 GB. Then commit on `feature/repo-consolidation`, then merge `origin/develop` (which brings `AGENTS.md` and `branch-policy.yml`).
- 🟡 **Apply Stage 5 Major 1.** Add a `bitrate` parameter to `efficient_video.render()` and `produce.video()` (default 160k). Re-encode the existing deliveries with a loop modeled on `update_title_previews.py`. Drop `renders/`, items 4–6, the `-compressed.json` schema (extend `reports/<k>-<mode>.json` instead), and the related Future Improvement.
- 🟡 **The guard compares the report `sha256` with the LFS pointer oid or the plain-file hash.** Skip any self-reported bitrate check.
- 🟡 **Sequence by bitrate certainty.** Commit full videos only after the 160k listening comparison against the FLAC; previews can go first. Add one `AGENTS.md` sentence: replacing a committed full video needs owner sign-off, because each replacement permanently adds about 0.6 GB of LFS. Drop the 650 MB goal and keep the 1 GB cap.
- 🟡 **Master regeneration gates deleting the masters, not merging.** CUJ 4 should say "same decoded PCM" (FLAC STREAMINFO MD5). Remove the literal `...` and name the seed source (the report). Add a Verification Plan gate: do not delete local masters until a 180 s preview regeneration matches. No new platform tracking.

## Proposals to reject or shrink

- **Pre-push hook: reject.** Unmatched masters would be plain blobs over GitHub's 100 MB limit and are rejected at push. After the bitrate change, nothing writes 320k files to tracked paths. Hooks are not installed by a clone. Record the rejection as one sentence under Alternatives.
- **Guard that walks commit history: replace it with squash-only merges on `develop`**, so the tip tree is exactly what lands. Keep merge commits for `develop` → `main`.
- **Risks table: keep it to about 5 rows**, each pointing to an existing mechanism: first-push leak, single-Mac masters, permanent LFS, tip-only guard, Pages cutover. Drop the admin-bypass, encoder-difference and bandwidth rows.
- **Pages alternatives: one sentence.** `docs/` holds the designs, and `gh-pages` or a separate repo would bring back the duplication.

## Small fixes to apply as written

Make the permissions consistent (252 vs. 366). Mark the files that exist only on `origin/develop`. Change the diagram's `git push` to `pull_request`. Fix the line 34 heading. Accept the duplicate posters because `site/` must be self-contained. State the value of the committed videos, or ask the owner whether v1.1.0 is their consumer.

# Stage 5 — Initial Zoom Out Review

Target: `docs/designs/repo-consolidation.md` (full file, 439 lines). Reviewer: `egm-zoom-out` (Goldfish, fresh context).

**Verdict:** Needs revision. 0 blockers, 4 major, 5 nits.

## 🟡 Major 1: `compress_videos.py` + `renders/` duplicate existing render code
Scope: Media flow (161–180), CUJ 1 (103–112), items 2, 4, 5, 6, Future Improvements.
`scripts/efficient_video.py` `render()` already stream-copies the title and black H.264 segments and encodes continuous AAC from the FLAC master. Only the bitrate (hard-coded 320k) differs; `produce.video()` hard-codes 320k too. `update_title_previews.py` already implements "re-render from master → video_qc → replace".
**Fix:** Add an audio-bitrate parameter to `efficient_video.render()` and `produce.video()`, default 160k, write directly to `videos/` / `site/media/`. Make the re-encode for existing masters a thin loop modeled on `update_title_previews.py`. Drop `renders/`, items 4–5, and the related Future Improvement. Re-anchor CUJ 1 on the master.

## 🟡 Major 2: CUJ 4 / Alternative C assume untested reproducibility and use a hash that won't reproduce
Scope: CUJ 4 (130–136), Alternative C (223–230), line 151.
Masters are written by ffmpeg, which stamps an encoder tag; the file SHA-256 changes with the ffmpeg version even if the samples match. The gain derivation depends on ffmpeg's loudnorm.
**Fix:** Compare a decoded-PCM hash (FLAC STREAMINFO MD5 or `-f md5`), record the ffmpeg version, and run one real preview-length regeneration in the Verification Plan. If it doesn't match, keep masters on disk / reopen Alternative C.

## 🟡 Major 3: `media-guard` checks the tip tree, but the rule covers history
Scope: Owner rules (52–54), guard (346–355), size audit (433–435).
A PR that adds then deletes a master passes the guard, and a non-squash merge keeps the blob forever.
**Fix:** Check every object the PR introduces (`git rev-list --objects base..head | git cat-file --batch-check`, plus LFS pointer parsing), or require squash merges.

## 🟡 Major 4: Two parallel report schemas
Scope: CUJ 1 (110), item 6, item 11.
`reports/<k>-<mode>.json` already contains `video_qc`, `video_encoding`, `sha256`; a second `-compressed.json` would leave the original describing an uncommitted 320k file.
**Fix:** One report per delivery; update `reports/<k>-<mode>.json` with bitrate, bytes, sha256; point the guard at it.

## 🟢 Nits
1. Committed compressed videos have no consumer while the site links to v1.0.0. Bring the v1.1.0 repoint into scope, or say they are archival.
2. Preview FLACs are also regenerable. Explain why they stay in LFS, or ignore them.
3. The duplicate title PNGs are listed in Problem 4 but not resolved.
4. Say why legacy `/docs` Pages publishing wasn't used (`docs/` holds designs).
5. `branch-policy.yml` and `AGENTS.md` are marked "(exists)" but exist only on `origin/develop`.

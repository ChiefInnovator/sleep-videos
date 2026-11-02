# Consolidated Goldfish Review — repo-consolidation design

Target: [`docs/designs/repo-consolidation.md`](../repo-consolidation.md). Mode: consolidated (stages 5–9 without checkpoints). Stage reports: [zoom out](zoom_out_report.md), [comprehension](comprehension_report.md), [critic](critic_report.md), [intermediate zoom out](intermediate_zoom_out_report.md), [implementation readiness](implementation_readiness_report.md).

## Elephant evidence gathered during review

- **Regeneration test (2026-11-02, ffmpeg 9.0.2, arm64).** Two 180 s preview masters were regenerated from seed. `brown-noise` decoded-PCM MD5 matches the committed `previews/brown-noise-preview.flac` exactly. `white-noise` matches exactly when the recorded `constant_gain_db` (−6.58) is reused. Re-measuring loudness under ffmpeg 9.0.2 gives −6.60. **Conclusion:** synthesis is deterministic. Regeneration must reuse the recorded gain, not re-measure it.
- `origin/develop` = `d7498dd` + `7988fc4` (`AGENTS.md`, `branch-policy.yml`). It shares history with local `main`.

## Action items

Stage 8's sizing is used where it conflicts with Stage 7.

### 🔴 Blockers

| # | Action | Sources |
|---|---|---|
| A1 | Give an ordered, command-level first-commit sequence. Unstage the masters, 320k videos, preview MP4s and zip **before** any commit; audit sizes; commit; then merge `origin/develop`. | S6, S8, S9 R-B1 |
| A2 | Split the plan into phases, each with an exit check. | S9 R-B2 |
| A3 | Reuse `produce.video()` / `efficient_video.render()` with a new `bitrate` parameter (default 160k) that writes straight to `videos/` and `site/media/`. A thin `compress_videos.py` loop re-encodes the existing masters. Drop `renders/` from the pipeline (the 320k files go to an ignored `renders/` only as a local archive). Drop the separate `-compressed.json` schema and extend `reports/<k>-<mode>.json` instead. This also fixes the missing `-t`, because the existing encoders pass it. | S5 M1, M4; S8; S9 R-B3 |
| A4 | Specify `media-guard.yml` as concrete YAML and shell. Compare the report `sha256` with the LFS oid or blob hash; reject `masters/`, `renders/`, anything over 1,000,000,000 bytes, LFS under `site/`, and stray MP4s. | S7 C-M4; S9 R-B4 |
| A5 | Add a short Risks & Mitigations section (5 rows). | S7 C-B1, S8 |
| A6 | CUJ 4 becomes "same decoded PCM, reusing the recorded gain", backed by the regeneration evidence above. Deleting local masters stays gated on that check. | S5 M2, S7 C-B2, S8 |

### 🟡 Major

| # | Action | Sources |
|---|---|---|
| A7 | Require squash merges into `develop` (tip-tree guard is then sufficient); keep merge commits for `develop` → `main`. No pre-push hook (rejection recorded under Alternatives). | S5 M3, S7 C-M3, S8 |
| A8 | Commit full videos only after a 160k listening check against the FLAC; previews may go first. Add an `AGENTS.md` note: replacing a full video needs owner sign-off (permanent LFS growth). | S7 C-M1, S8 |
| A9 | Drop the 650 MB goal; keep 1,000,000,000 bytes as the only cap, checked before QC. Restate expected sizes (about 600–625 MB). | S7 C-M2, S9 R-M4, R-M11 |
| A10 | Define "compressed" (the AAC bitrate the compression step set), fix the line 34 heading, define `<kind>` and `<mode>`, and list the five kinds. | S6, S7 C-M6, S9 R-M11 |
| A11 | Make the permissions consistent, and give the full `pages.yml` (environment, pinned actions, concurrency). | S6, S7 C-M10, S9 R-M5 |
| A12 | Give exact `gh api` commands for the Pages `build_type`, rollback, rulesets (squash-only plus the `media-guard` check), and their timing. | S9 R-M6 |
| A13 | Expand the verification plan to cover every guard rule, the compressor failure path, regeneration, `Content-Length`, a working size-audit command, and mandatory `actionlint`. | S9 R-M7, R-M10, R-M12 |
| A14 | Document the `video_qc` contract: `.venv/bin/python`, the verifier binary, the `.rgb-framemd5` sidecars, and patching `probe.filename`. | S6, S9 R-M1 |
| A15 | Ignore `*.tmp.mp4` and the source zip; drop `*.uncompressed.mp4`. | S9 R-M2 |
| A16 | Mark the v1.0.0 hash evidence (`full-artifact-hashes.json`, `SHA256SUMS`) as describing the release assets. | S9 R-M9 |
| A17 | Give the target text for the README, `site/README.md`, `review.html` and `AGENTS.md` edits. | S9 R-M8 |
| A18 | Fix the Alternative B rejection reason; add one-line alternatives for the Pages method and the enforcement point; state the value of the committed videos (source for v1.1.0, tied to the commit). | S7 C-M5, C-M8, S8 |
| A19 | Remove unsourced absolutes (no downtime, transparency, masking, Opus); label files as "(on `origin/develop`)"; accept the duplicate posters (`site/` is self-contained); fix heading levels. | S6, S7 C-M7, C-M9, C-M12, C-M13 |

### 🟢 Nits

Use `<kind>` consistently, link text, horizontal-rule consistency, Open Questions placement, the bandwidth figure, filler words, the `pull_request` arrow in the diagram, `produce.py:272` references, reusing `digest()`, copying the poster for title revisions.

## Traceability

Every Stage 5–9 finding maps to A1–A19 or to the nit list. Rejected or shrunk per Stage 8: the pre-push hook (A7), the history-walking guard (A7), the lifetime LFS budget policy (A8), the admin-bypass / encoder-difference / bandwidth risk rows (A5), and the self-reported bitrate check (A4).

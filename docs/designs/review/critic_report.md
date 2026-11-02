# Stage 7 — Critic Review

Target: `docs/designs/repo-consolidation.md`, FeatureRange 1–275. Reviewers: `egm-design`, `egm-structural` (feature-spec-standard), `egm-style`. Duplicate findings are merged; the sources are listed in brackets.

## 🔴 Blockers

- **C-B1: No Risks & Mitigations section.** [design, structural] Risks are scattered across Open Questions, the Pages cutover text, and the NFRs. Missing risks: masters exist only on one Mac; pushed LFS storage cannot be removed; the guard sees only the final tree; LFS bandwidth runs out on full clones; a direct push or admin bypass skips the guard; `aac_at` and native `aac` give different output by machine; the Pages rollback. **Fix:** add a `## Risks & Mitigations` table (Risk | Impact | Mitigation).
- **C-B2: Byte-identical master regeneration is assumed, not proven.** [design] ffmpeg 9.0.1 writes the FLAC and measures the gain but is not pinned. Floating-point results can also vary by platform. Nobody has ever run a regeneration. **Fix:** record the ffmpeg version, platform and arch; compare decoded PCM rather than the container; run a 180 s preview regeneration and compare it with the preview FLAC in LFS before untracking masters. If it fails, reopen Alternative C.

## 🟡 Major

- **C-M1: LFS storage is permanent, and the plan commits before the bitrate is settled.** [design] A 192k re-encode adds about 3.5 GB that can never be reclaimed. **Fix:** commit the full videos only after a 160k listening check against the FLAC; add a lifetime LFS budget and a re-render policy.
- **C-M2: The 650 MB goal contradicts the 192 kb/s fallback (~720 MB).** [design, structural] **Fix:** tie the size expectation to the bitrate, with 1 GB as the hard cap.
- **C-M3: The guard checks the final tree only, not the history the rule covers.** [design] **Fix:** walk `base..head` objects with `fetch-depth: 0`; add a local `pre-push` hook (the only thing that stops the LFS upload).
- **C-M4: The "compressed" check proves only that the size matches.** [design] **Fix:** compare the report's `sha256` with the LFS pointer oid (and with the blob hash for `site/media`); check that `bitrate` is at most the agreed value.
- **C-M5: Alternative B's rejection is preference only and partly inaccurate; the committed videos have no consumer.** [design, structural] Releases *are* tied to tags. **Fix:** state the concrete value of committing them, or bring the v1.1.0 repoint into scope.
- **C-M6: "Uncompressed" is wrong.** The 320k AAC is already compressed, and the line 34 heading is garbled. [design, structural, style] **Fix:** define "compressed" as produced by the compression step at or below the agreed bitrate; reword.
- **C-M7: Problem 4's duplicates (posters, zip) have no Goal.** [structural] **Fix:** add a Goal, or make it a Non-Goal with a reason.
- **C-M8: Alternatives cover storage only.** [structural] **Fix:** add Pages deployment (`/docs` folder, `gh-pages`, separate repo) and enforcement point (CI only vs. hook).
- **C-M9: Absolute or unsourced claims.** These are "no downtime" / "no request sees a missing page", "transparent-for-most-listeners", "no masking structure", and the vague Opus claims. [style] **Fix:** state the mechanism instead of a guarantee, and cite a source or drop the claim.
- **C-M10: The NFR permissions contradict item 8 (`contents: read`).** [style] **Fix:** each workflow sets `permissions: {}`, and every grant is listed explicitly.
- **C-M11: Goals list 2 checks and CUJ 1 lists 4.** [style] **Fix:** name the `video_qc` set once.
- **C-M12: Files marked "(exists)" are missing locally.** [structural] **Fix:** "(on `origin/develop`)".
- **C-M13: Additional Resources and Future Improvements are H3s nested under the NFR.** [structural, style] **Fix:** promote both to H2.

## 🟢 Nits

Mixed GB/GiB units (state 1 GB = 10^9 bytes). Inconsistent `<k>`/`<kind>` naming and file-name schemes in the diagrams. Bare URLs. Inconsistent horizontal rules. Open Questions placed before the concepts they reference. No bandwidth quota figure. "Currently" and other filler. "Rich" vs. "owner" used interchangeably. "Every-frame black" is ambiguous. The cutover claim has no source. The `verify-black-frames` prerequisite and the `.rgb-framemd5` sidecars are not listed. The 3.0 → 3.1 GB arithmetic.

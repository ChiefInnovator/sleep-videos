# Stage 6 — Comprehension Test

Target: `docs/designs/repo-consolidation.md`. FeatureRange 1–275, DetailedRange 276–439. Reviewer: `egm-comprehension` (Goldfish).

## What this proposes

The design turns a large restructure, currently staged but not committed in the local clone, into a change that can be merged. Lossless FLAC masters and the 320 kb/s renders stay out of Git as ignored local files. A new script, `scripts/compress_videos.py`, builds the files that do get committed: it copies the H.264 video stream from the render, re-encodes the audio from the FLAC master to 160 kb/s AAC, and re-runs the QC checks from `produce.py`. Full videos go to `videos/` in LFS. Previews go to `site/media/` as plain Git blobs, so that Pages can serve them. A new `media-guard` PR check enforces a 1 GB per-file ceiling, keeps `masters/` out, rejects LFS files under `site/`, and requires a matching compression report for each video. Pages moves from serving the root of `main` to a `pages.yml` Actions workflow that deploys `site/`.

## How the existing system works, per this document

Today the public repo holds only the marketing site at the root of `main`, and GitHub Pages serves it as a branch deployment. `produce.py` synthesizes each soundscape from a seed. It writes a 24-bit FLAC master and an MP4 with 320 kb/s AAC audio, a title for about six seconds, then black video. It runs duration, black-frame, true-peak and decoded-audio checks on the MP4. The eight-hour downloads are v1.0.0 GitHub Release assets that the site links to. The local staged restructure would push about 27 GB through LFS. That fails on the 2 GB per-file limit and the quota, and moving `index.html` would also break Pages.

## Findings

- 🟡 **278–281: the branch's starting state is unclear.** Staged changes are not on any branch, and the text does not say when the first commit happens or whether the item 3 unstaging comes before it. Committing first would put the masters into history. **Fix:** list the steps in order: unstage, then commit on `feature/repo-consolidation`, then merge `origin/develop`. Also say what `develop` brings in.
- 🟡 **145, 148, 248–249: files marked "(exists)" are missing locally.** `AGENTS.md` and `branch-policy.yml` are only on `origin/develop`. **Fix:** say so.
- 🟡 **333–336: the `produce.video_qc` contract is misdescribed.** It returns a dict and does not write JSON. It uses `report` only for the `.rgb-framemd5` sidecar on previews. Full-length runs need `.venv/bin/verify-black-frames`, which the doc never mentions. **Fix:** say that the script writes the JSON itself, name the sidecar, and add the verifier build as a prerequisite.
- 🟡 **42–45 vs. 149, 158: the duplicate title PNGs are never resolved.** **Fix:** remove one copy, or accept the duplicate and say why (for example, `site/` must be self-contained).
- 🟡 **130–136: CUJ 4 cannot be followed.** It has a literal `...`, does not say where the seed comes from, and leaves ffmpeg/flac versions unpinned. That undermines the reason Alternative C was rejected. **Fix:** give the full command and the seed source, and either pin the tool versions or weaken the claim to "same decoded PCM".
- 🟡 **252–253 vs. 366–367: the permissions disagree.** The NFR omits `contents: read`, which `media-guard` also needs. **Fix:** make the two lists match and give the guard its permissions explicitly.
- 🟢 **173:** the diagram says `git push`, but the guard runs on `pull_request`.
- 🟢 **65–67 vs. 352:** the Goals cover any MP4 under `videos/` or `site/media/`, but the plan checks only `*-full.mp4` and `*-preview.mp4`.
- 🟢 **109, 334:** "every-frame black" is ambiguous. Say "every frame after the title".
- 🟢 **153:** the reason preview FLACs stay in LFS is missing.
- 🟢 **84:** "Impeccable pass", `PRODUCT.md`, and `DESIGN.md` are undefined.
- 🟢 **120, 357–358:** rulesets are referenced before they are introduced, and the IDs are not mapped to branches.
- 🟢 **105–107, 171:** `<kind>`, `<k>`, and `<mode>` are undefined, and the five kinds are not listed.
- 🟢 **34:** "Committed uncompressed for the purpose" does not parse clearly.
- 🟢 **32–33:** no figure is given for the LFS bandwidth quota.
- 🟢 **197–201:** the cutover claim has no source, and the rollback via revert ignores the branch rulesets.

No blockers: every section could be paraphrased.

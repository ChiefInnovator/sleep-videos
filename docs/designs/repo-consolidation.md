# Sleep Soundscapes: Repository Consolidation and Compressed Media Delivery

*   **Author:** Rich Crane (ChiefInnovator)
*   **Status:** Approved (Goldfish review applied; see [review/consolidated_review_report.md](review/consolidated_review_report.md))
*   **Date:** 2026-11-02

## Overview

The `ChiefInnovator/sleep-videos` repository publishes only the marketing site.
Its `index.html`, `styles.css`, `app.js`, and `media/` sit at the root of
`main`, and GitHub Pages serves that root. The production workspace exists only
on the owner's Mac: the synthesis scripts, reports, previews, eight-hour videos,
and lossless masters.

Since 2026-09-14, the local clone has held a staged, uncommitted restructure. It
moves the site into `site/` and adds the whole production workspace, including
about 27 GB of media through Git LFS. That restructure cannot be pushed as
staged. If it were merged, it would take the public site offline.

This design turns the staged restructure into a change that can be merged. It
defines which media may enter Git, requires a compression step before any video
is committed, caps every tracked file at 1 GB, and moves Pages publishing to a
GitHub Actions deployment of `site/`.

**Terms.**

*   **Kinds**: the five soundscapes `white-noise`, `distant-thunder-rain`,
    `rain-on-window`, `brown-noise`, and `ambient-drone`. `<kind>` stands for
    one of them.
*   **Modes**: `<mode>` is `preview` (180 s) or `full` (28,800 s).
*   **GB**: 1 GB means 1,000,000,000 bytes.
*   **Compressed**: a video is compressed when `scripts/compress_videos.py`
    wrote it from the FLAC master at the configured AAC bitrate, default
    160 kb/s. The script records the file's SHA-256 in
    `reports/<kind>-<mode>.json`.

## The Problem

1.  **Files exceed what the repository can hold.** Four of the five FLAC masters
    are 2.3 to 6.4 GB (decimal). GitHub LFS rejects files over 2 GB on this
    plan, so the push fails. Staged media totals about 27 GB, against free LFS
    quotas of 10 GB storage and 10 GB of bandwidth per month.
2.  **Videos carry more audio bitrate than the content needs.** Each eight-hour
    MP4 is 1.18 to 1.22 GB. The picture is black after six seconds, so almost
    all of the size is 320 kb/s AAC audio. No listening test has shown that
    320 kb/s sounds better than a lower bitrate for these signals.
3.  **Pages would break on merge.** The restructure moves `index.html` from the
    root into `site/`. Pages publishes the root of `main`, so the merged site
    would return 404.
4.  **Duplicate and stale content.** `previews/*.mp4` and `site/media/*.mp4` are
    byte-identical. `reports/sleep-soundscapes-v1.0.0-source.zip` duplicates a
    release asset. `README.md` describes `site/` as a separate repository,
    `site/README.md` says that Pages publishes the root, and `review.html` says
    the eight-hour videos have not been rendered. All three statements are now
    false.

Owner rules that bound the solution:

*   Videos are always compressed before they are checked into Git.
*   No tracked file may exceed 1 GB.

## Goals

*   The restructure merges through `feature/*` → `develop` → `main` with no
    object over 1 GB in the merged history.
*   Every committed MP4 is compressed (see Terms), and it passes the existing
    `produce.video_qc` checks: duration, frame count, black pixels after the
    six-second title, true peak at or below −2 dBTP, and decoded-AAC screening.
*   A required `media-guard` check fails any pull request that tracks a file
    under `masters/` or `renders/`, tracks an object over 1 GB, puts an LFS
    pointer under `site/`, or tracks an MP4 whose SHA-256 does not match its
    report.
*   https://chiefinnovator.github.io/sleep-videos/ returns 200 before and after
    the cutover, now deployed from `site/` by a workflow.
*   Stale statements in `README.md`, `site/README.md`, and `review.html` are
    corrected, and the duplicate preview MP4s and the source zip leave the
    index.

## Non-Goals

*   Changing synthesis, mastering levels, fades, or title timing.
*   Replacing the v1.0.0 GitHub Release. The site keeps linking to it until a
    v1.1.0 release is cut from the compressed videos (see Open Questions).
*   Deleting local masters or the 320 kb/s videos. They become ignored files.
    Deleting them is the owner's decision. Before any deletion, a regeneration
    match must be confirmed (CUJ 4).
*   Redesigning the site. Visual work follows the Impeccable workflow, which
    reads `PRODUCT.md` and `DESIGN.md` at the repository root.
*   Completing the listening review.

## Critical User Journeys (CUJs)

### CUJ 1: Produce a committable video

*   **Given**: `masters/<kind>-full.flac` (or `previews/<kind>-preview.flac`)
    exists, and `.venv` plus `.venv/bin/verify-black-frames` are built as
    described in the README.
*   **When**: The owner runs
    `.venv/bin/python scripts/compress_videos.py [--full] [--only <kind>]`.
*   **Then**: `videos/<kind>-full.mp4` (or `site/media/<kind>-preview.mp4`) is
    written at 160 kb/s AAC. The script refuses any output over 1 GB before it
    runs the QC checks. It then runs `video_qc` and updates
    `reports/<kind>-<mode>.json` with the delivery bitrate, encoder, bytes,
    SHA-256, and QC results. If any check fails, the script exits non-zero,
    removes its temporary file, and leaves the target and the report unchanged.

### CUJ 2: Attempt to commit an oversized or unverified file

*   **Given**: A feature branch tracks `masters/x.flac`, an object over 1 GB, or
    an MP4 whose SHA-256 does not match its report.
*   **When**: A pull request into `develop` opens.
*   **Then**: The `media-guard` check fails and names the file and the rule it
    broke. The `develop` ruleset blocks the merge.

### CUJ 3: Ship the site after the restructure

*   **Given**: The restructure merges from `develop` into `main`, and Pages is
    set to deploy from GitHub Actions.
*   **When**: `pages.yml` runs on the push to `main`.
*   **Then**: `site/` deploys. `/`, `/app.js`, and
    `/media/white-noise-preview.mp4` return 200. The preview's `Content-Length`
    equals the `delivery.bytes` value in its report, not the size of an LFS
    pointer.

### CUJ 4: Regenerate a master

*   **Given**: The masters are not in Git. Each report records the master's
    `seed` and `constant_gain_db`.
*   **When**: The owner synthesizes `<kind>` with `produce.generate(kind, seed,
    seconds, raw)` and applies the **recorded** gain with the same FFmpeg FLAC
    command as `produce.py`.
*   **Then**: The decoded PCM MD5 (`ffmpeg -i <flac> -f md5 -`) equals that of
    the original master. This was verified on 2026-11-02 for the brown-noise
    and white-noise previews, using FFmpeg 9.0.2 on arm64; the originals were
    made with 9.0.1. Re-measuring the gain instead of reusing it moved
    white-noise by 0.02 dB and broke the match. File-level SHA-256 is not
    expected to match across FFmpeg versions.

## Technical Plan (Architecture)

### Repository layout after merge

```text
/
├── .github/workflows/
│   ├── branch-policy.yml  (on origin/develop) PR source-branch rule
│   ├── media-guard.yml    (new) tracked-media rules
│   └── pages.yml          (new) deploy site/ to Pages
├── AGENTS.md              (on origin/develop) branch + media rules
├── PRODUCT.md, DESIGN.md  Impeccable product and design context
├── assets/                title art (PNG, small)
├── docs/designs/          this design and its review reports
├── masters/               IGNORED: lossless FLAC, regenerable (CUJ 4)
├── renders/               IGNORED: local archive of the v1.0.0 320k MP4s
├── previews/              <kind>-preview.flac in LFS; *.mp4 IGNORED
├── videos/                <kind>-full.mp4, compressed, LFS, ≤ 1 GB
├── reports/               production sheets, logs, hashes
├── scripts/               produce.py, compress_videos.py, verify_*
└── site/                  published by pages.yml; plain Git, no LFS
    └── media/             compressed previews + title posters
```

Preview FLACs stay in LFS (about 130 MB in total). They are the source for the
committed site previews, and `review.html` links to them. The title posters
exist in both `assets/` and `site/media/` on purpose: `site/` is uploaded on
its own as the Pages artifact, so it must be self-contained.

### Media flow

```text
produce.py ─► masters/<kind>-full.flac        (24-bit, ignored)
          └─► previews/<kind>-preview.flac    (LFS)
                         │
compress_videos.py ◄─────┘  produce.video(master, tmp, seconds, kind,
          │                   efficient=full, bitrate='160k')
          ├─► videos/<kind>-full.mp4          (LFS)
          ├─► site/media/<kind>-preview.mp4   (plain Git, ~3.7 MB)
          └─► reports/<kind>-<mode>.json      (delivery: bitrate, bytes, sha256)
                         │
pull_request ─► media-guard.yml ─► required check on develop and main
```

`produce.video()` and `efficient_video.render()` gain a `bitrate` parameter that
defaults to `'160k'`. Both already encode audio directly from the FLAC master
and pass `-t <seconds>`, so the output has a single lossy generation and an
exact duration. `produce.py --full` therefore writes compressed videos to
`videos/` from now on. `compress_videos.py` re-encodes deliveries from masters
that already exist, using the same loop as `update_title_previews.py`.

### Enforcement

*   **`media-guard`** reads Git objects, not the working tree. For each entry in
    `git ls-files -s`, it reads the blob with `git cat-file blob`. If the blob
    is an LFS pointer, it takes `size` and `oid` from the pointer. Otherwise it
    uses the blob's own size and SHA-256. No LFS content is downloaded.
*   **Squash merges into `develop`.** Each feature PR lands as a single commit,
    so a file added and then removed inside a PR never enters history. The tree
    check is therefore enough. `develop` → `main` keeps merge commits.
*   **Rulesets.** Ruleset 26358790 ("develop: PRs from feature/* only + Copilot
    review") and ruleset 26358788 ("main: PRs from develop only") both require
    `source-branch` and `media-guard`. Copilot code review runs only on
    `develop`.

### Pages cutover

Legacy Pages can publish only `/` or `/docs`, and `docs/` holds the design
documents. Pages therefore switches to a GitHub Actions deployment. The switch
(`build_type: workflow`) happens immediately before the `develop` → `main`
merge. The merge triggers `pages.yml`, which replaces the previous deployment
when it finishes. Rollback: restore `build_type: legacy` with source
`main:/`, then merge a `feature/*` → `develop` → `main` revert, since direct
pushes to `main` are blocked.

## Alternatives Considered

### Alternative A: Commit everything to LFS as staged

*   **Pros**: No new scripts. Masters are versioned with the code.
*   **Cons**: Four masters exceed the 2 GB LFS per-file limit, so the push
    fails. About 27 GB exceeds the storage quota.
*   **Reason for Rejection**: It cannot be pushed, and it violates the 1 GB
    owner rule.

### Alternative B: Keep the full videos only in GitHub Releases

*   **Pros**: The repository stays small, and release downloads do not use LFS
    bandwidth.
*   **Cons**: Release assets can be replaced without a commit, so the
    `media-guard` hash check cannot cover them. The owner requires compressed
    videos to live in Git.
*   **Reason for Rejection**: Committing the compressed videos ties each one to
    the commit and report that produced it, and makes them the source for
    v1.1.0.

### Alternative C: Archive masters in Azure Blob Storage

*   **Pros**: An off-machine lossless copy.
*   **Cons**: Adds an Azure dependency and a monthly cost for files that CUJ 4
    shows can be regenerated.
*   **Reason for Rejection**: Not needed while regeneration matches. Revisit if
    it stops matching.

### Alternative D: Re-encode audio with Opus

*   **Pros**: Smaller files at a similar perceived quality.
*   **Cons**: Not all download targets (TVs, older players) decode Opus in MP4.
*   **Reason for Rejection**: AAC-LC in MP4 plays everywhere the v1.0.0 files
    already play, and it meets the size cap.

### Alternative E: Other Pages publishing methods

*   **Cons**: `/docs` publishing collides with the design documents. A
    `gh-pages` branch or a separate site repository brings back the duplicate
    copies this design removes.
*   **Reason for Rejection**: A workflow deployment of `site/` has neither
    problem.

### Alternative F: A local pre-push hook in addition to CI

*   **Cons**: Hooks are not installed by `git clone`. Once masters and renders
    are ignored, the remaining risk is the one-time first commit, and Phase 1's
    checklist covers that. Plain blobs over 100 MB are rejected by GitHub at
    push time anyway.
*   **Reason for Rejection**: It adds setup steps for almost no protection.

## Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| The first commit captures the staged masters or the 320k videos | Permanent LFS storage use, or a failed push | Phase 1 ordered checklist with an index size audit before the commit |
| Masters exist on one Mac only | No lossless source if the disk is lost | CUJ 4 regeneration, verified for previews; masters are deleted only after a full-length match |
| LFS storage cannot be reclaimed | Each replacement of a full video permanently adds about 0.6 GB | Full videos are committed only after a 160k listening check; replacing one needs owner sign-off (`AGENTS.md`) |
| The guard sees only the PR's final tree | A file added and removed within a PR could enter history | Squash-only merges into `develop` |
| Pages cutover fails | The site is down | Switch `build_type` immediately before the merge; documented rollback |

## Open Questions

*   **Audio bitrate**: 160 kb/s AAC-LC is the default. It has not been confirmed
    by listening on these noise signals. If artifacts are heard, 192 kb/s
    (about 720 MB for eight hours) still fits under the cap.
*   **v1.1.0 release**: Should the compressed videos replace the 320 kb/s
    release assets as the public downloads? Each download would shrink from
    about 1.2 GB to about 0.6 GB.

## Non-Functional Requirements

*   **Storage and bandwidth**: Expected LFS storage is about 3.2 GB: five full
    videos at about 0.6 GB each, plus about 130 MB of preview FLACs. To skip
    video downloads, clone with `GIT_LFS_SKIP_SMUDGE=1` or set
    `lfs.fetchexclude=videos/`.
*   **Security**: Each workflow declares top-level `permissions` with only what
    it needs. `branch-policy.yml` grants none (`{}`), `media-guard.yml` grants
    `contents: read`, and `pages.yml` grants `contents: read`, `pages: write`,
    and `id-token: write`. No secrets are committed, and `.env*`
    stays ignored.

## Additional Resources

*   [About Git Large File Storage](https://docs.github.com/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
*   [Using custom workflows with GitHub Pages](https://docs.github.com/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
*   `reports/full-summary.md`, `reports/listening-review.md`, `production-prompt.md`

## Detailed Implementation Plan

### Phase 1: Clean the index and commit the restructure

Run these from the local clone, with the staged restructure present.

1.  `git switch -c feature/repo-consolidation`. The staged index comes along
    with the switch.
2.  `git rm --cached -r -q masters videos` and
    `git rm --cached -q previews/*.mp4 reports/sleep-soundscapes-v1.0.0-source.zip`.
3.  `mkdir -p renders && mv videos/*-full.mp4 renders/` keeps the v1.0.0 files
    locally and ignored.
4.  Edit `.gitattributes`: remove `/masters/*.flac` and `/previews/*.mp4`;
    keep `/previews/*.flac` and `/videos/*.mp4`.
5.  Append to `.gitignore`: `/masters/`, `/renders/`, `/previews/*.mp4`,
    `*.tmp.mp4`, `/reports/sleep-soundscapes-v1.0.0-source.zip`.
6.  Size audit: `git ls-files -s | awk '{print $2}' | git cat-file
    --batch-check='%(objectsize) %(objectname)' | sort -n | tail -3` shows
    nothing over 1,000,000,000. `git lfs ls-files` lists only
    `previews/*.flac`.
7.  Commit, then run `git merge origin/develop`. `develop` adds `AGENTS.md` and
    `branch-policy.yml`. `origin/develop` shares history with local `main` at
    `d7498dd`.

**Exit check:** step 6 passes on `HEAD`.

### Phase 2: Script changes

#### `scripts/efficient_video.py` (Modify)

`render(master, output, seconds, kind, bitrate='160k')`: replace the
hard-coded `'320k'` with `bitrate`.

#### `scripts/produce.py` (Modify)

*   `video(master, output, seconds, kind, efficient=False, bitrate='160k')`:
    replace `'320k'` with `bitrate`, and pass `bitrate` to `render`.
*   The `video_encoding` text in the report uses the actual bitrate rather than
    "320 kb/s".

#### `scripts/compress_videos.py` (Create)

*   CLI: `[--full] [--only KIND] [--bitrate 160k]`.
*   For each kind:
    *   The master is `masters/<kind>-full.flac` with `--full`, otherwise
        `previews/<kind>-preview.flac`.
    *   The target is `videos/<kind>-full.mp4` with `--full`, otherwise
        `site/media/<kind>-preview.mp4`.
    *   The temp file is `target.with_suffix('.tmp.mp4')`.
*   The script calls `produce.video(master, tmp, seconds, kind,
    efficient=full, bitrate=bitrate)`. It fails if
    `tmp.stat().st_size > 1_000_000_000`. Then it runs `video_qc(tmp, seconds,
    report_path)`, sets `qc['probe']['format']['filename']` to the target path,
    and calls `tmp.replace(target)`.
*   It then updates `reports/<kind>-<mode>.json`:
    *   `video_qc` becomes the new QC result.
    *   `video_encoding` describes the new encode.
    *   `delivery` becomes `{"bitrate": "160k", "encoder": "aac_at" | "aac",
        "bytes": <int>, "sha256": "<lowercase hex>", "path":
        "<repo-relative target>"}`.
    *   The stale `sha256` key is removed.
*   On any exception, the script deletes `tmp` and exits non-zero.
*   Preview runs also rewrite `reports/<kind>-preview.rgb-framemd5`.

### Phase 3: Compress and commit the previews

1.  `.venv/bin/python scripts/compress_videos.py` produces five previews
    (about 3.7 MB each).
2.  Commit `site/media/*.mp4`, `reports/*-preview.json`, and
    `reports/*-preview.rgb-framemd5`.
3.  Run `.venv/bin/python scripts/compress_videos.py --full` locally (several
    hours) to measure the real sizes. Do not commit `videos/` until the owner
    has done the 160k listening check.

**Exit check:** five reports with `delivery.bytes` < 1,000,000,000 and every
QC assertion passing.

### Phase 4: Workflows and documentation

#### `.github/workflows/media-guard.yml` (Create)

*   Trigger: `pull_request` into `main` and `develop`.
*   Permissions: `contents: read` only.
*   Job: a single job named `media-guard` on `ubuntu-latest`. It runs
    `actions/checkout@v4` (no LFS) and then a bash script with the rules below.
    Each failure prints `::error file=<path>::<rule>`, and the job fails at the
    end if any rule failed.
*   For every `mode oid stage path` entry from `git ls-files -s`:
    1.  A path under `masters/` or `renders/` fails.
    2.  If `git cat-file blob <oid>` starts with
        `version https://git-lfs.github.com/spec/v1`, the entry is LFS. Its size
        and sha come from the `size` and `oid sha256:` lines. Otherwise, the
        size comes from `git cat-file -s` and the sha from
        `git cat-file blob <oid> | sha256sum`.
    3.  A size over 1,000,000,000 fails.
    4.  An LFS entry under `site/` fails.
    5.  A `*.mp4` path must match `^videos/(.+)-full\.mp4$` or
        `^site/media/(.+)-preview\.mp4$`. The matching
        `reports/<kind>-<mode>.json` must exist, and its `delivery.sha256` (read
        with `jq`) must equal the computed sha. Any other `*.mp4` fails.

#### `.github/workflows/pages.yml` (Create)

*   Trigger: `push` to `main`, and `workflow_dispatch`.
*   Permissions: `contents: read`, `pages: write`, `id-token: write`.
*   Concurrency: group `pages`, `cancel-in-progress: false`.
*   Job `deploy`: runs on `ubuntu-latest` in environment `github-pages` (url
    `${{ steps.deployment.outputs.page_url }}`). Its steps are
    `actions/checkout@v4`, `actions/configure-pages@v5`,
    `actions/upload-pages-artifact@v3` with `path: site`, and
    `actions/deploy-pages@v4` with `id: deployment`.

#### `AGENTS.md` (Modify)

Add:

*   Videos are committed only after `scripts/compress_videos.py`.
*   No tracked file may exceed 1,000,000,000 bytes.
*   `masters/` and `renders/` are never tracked.
*   Nothing under `site/` may be in LFS.
*   Replacing a committed full video requires owner sign-off.
*   To clone without the videos, use `GIT_LFS_SKIP_SMUDGE=1`.
*   `EGM artifact directory: docs/designs/review`.

#### `README.md` (Modify)

*   **Line 3:** describe the single repository, with `site/` deployed by
    `pages.yml`.
*   **Line 13:** say the v1.0.0 320k MP4s are archived in ignored `renders/`;
    committed videos are compressed and live in `videos/`; masters are ignored
    and can be regenerated (CUJ 4).
*   **Production steps:** add `compress_videos.py`, and say that
    `produce.py --full` now writes 160k videos.

#### `site/README.md` (Modify)

*   Pages deploys `site/` through `.github/workflows/pages.yml`.
*   To update a preview, run `compress_videos.py`, and copy a changed title
    poster from `assets/` into `site/media/`.

#### `review.html` (Modify)

*   Replace "These are previews; the eight-hour videos have not been rendered."
    with "Full eight-hour videos are on the v1.0.0 release."
*   Change the video `src` to `site/media/${id}-preview.mp4?v=160k`.

#### `reports/SHA256SUMS`, `reports/full-artifact-hashes.json` (Leave as is)

They record the v1.0.0 release assets. The README states this.

### Phase 5: Merge into develop and update the rulesets

1.  Push `feature/repo-consolidation` and open a PR into `develop`.
2.  After the `media-guard` workflow file exists on the PR branch, update both
    rulesets with `gh api -X PUT repos/ChiefInnovator/sleep-videos/rulesets/<id>
    --input <json>`. Add `{"context":"media-guard","integration_id":15368}` to
    `required_status_checks`. On ruleset 26358790, set
    `allowed_merge_methods` to `["squash"]`.
3.  Address the Copilot review, then squash-merge.

### Phase 6: Pages cutover and release to main

1.  `gh api -X PUT repos/ChiefInnovator/sleep-videos/pages -f build_type=workflow`.
2.  Open a PR from `develop` into `main` and merge it with a merge commit.
3.  Verify CUJ 3.

### Verification Plan

*   **Static checks:** `python3 -m py_compile scripts/*.py`, and
    `actionlint .github/workflows/*.yml` exits 0.
*   **Compressor:** Phase 3 exit check. Failure path: run with
    `--bitrate 999999k` on one preview. It must fail the size cap or QC, exit
    non-zero, leave no `*.tmp.mp4`, and leave the target and report unchanged.
*   **Guard, negative cases:** on a branch `feature/media-guard-negative`, open
    a draft PR into `develop` with these commits, one at a time:
    1.  `masters/x.flac`
    2.  a hand-written LFS pointer at `videos/x-full.mp4` with
        `size 1000000001`
    3.  `site/media/x-preview.mp4` with no report

    Confirm that each fails `media-guard` with the expected message. Close the
    PR unmerged and delete the branch.
*   **Guard, positive case:** the Phase 5 PR passes.
*   **Pages:** CUJ 3, via `curl -sI` for each URL.
*   **Regeneration:** CUJ 4 (done for two previews on 2026-11-02).
*   **Size audit:** Phase 1 step 6, run on `main` after the merge.

*Drafted with EGM*

# Sleep video production

Marketing site: [Sleep Soundscapes](https://chiefinnovator.github.io/sleep-videos/). This repository holds both the production workspace and the site. The site lives in `site/` and is deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`. Repository layout, media rules and the branch flow are described in [the consolidation design](docs/designs/repo-consolidation.md) and `AGENTS.md`.

The production brief and current audio directions are in `production-prompt.md`.

User-requested revision: each video now opens with its own title and a smaller Inventing Fire with AI logo beneath it. The title holds from 00:00 to 00:04, fades to black by 00:06, and remains completely black afterward. This replaces the original brief's no-introduction requirement. The opening is included in the existing duration; audio starts at 00:00 with its existing gentle fade. The generator applies this opening to future full-length renders too.

## What has been produced

All five full deliveries passed automated verification. See [full technical results](reports/full-summary.md) and [the GitHub release](https://github.com/ChiefInnovator/sleep-videos/releases/tag/v1.0.0). Critical listening remains pending.

Five eight-hour soundscapes have been rendered: the v1.0.0 release MP4s (320 kb/s AAC) are archived locally in the ignored `renders/` folder, and the 48 kHz/24-bit stereo FLAC masters are in the ignored `masters/` folder. Masters are not committed; reports record the seed, constant gain and source checksums needed to reproduce the production process. Videos committed to `videos/` are re-encoded from the masters at 160 kb/s by `scripts/compress_videos.py`. Every full file is exactly 8:00:00. The videos use 1280×720 at 24 fps, with AAC encoding configured at 320 kb/s for v1.0.0. Matching three-minute previews (160 kb/s) are in `site/media/`, with their FLAC masters in `previews/`; open `review.html` to play them. Each includes a two-second raised-cosine audio fade-in and a 25-second fade-out. The same fade durations apply to the eight-hour renders, replacing the original brief's 20–30-second opening fade at the user's request.

The revised weather tracks use licensed real recordings. Thunder passages retain their native cadence and play sequentially, with no added thunder overlap or generated cracks. Window rain uses calm recorded excerpts over recorded rain. Finite source passages are reused in varied order; these are constructed mixes, not continuous eight-hour field captures. Sources and licenses are in [the source manifest](assets/recordings/sources.json), with [published credits](site/recording-credits.txt). White noise, brown noise and the drone remain original synthesis. Listening approval of the real-thunder audition does not replace full-length critical listening.

`reports/*-preview.json` contains each production sheet: source provenance, synthesis method, seed, processing, loudness, true peak, loudness range, one-second RMS measurements, title timing, and verification of every decoded RGB video frame after the title. `reports/preview-run.log` records the original audio run; `reports/title-update.log` records the branded video revision. `reports/*-preview.rgb-framemd5` retains the current per-frame evidence. The loudnorm JSON **input** fields are the measurements of the delivered file; its output fields describe the analyzer's discarded processing and are not delivery measurements.

## Listening evaluation — pending

The current agent has no audio-listening tool. Numerical checks do not establish comfortable listening, realism, absence of perceptible repetition, or lack of codec artifacts. The user explicitly requested the full renders on 2026-09-14 while this listening evaluation remained pending. Generation proceeded with `--render-without-listening-review`; no listening pass is asserted.

1. Open `review.html` and listen to all five previews at a comfortable volume on headphones. Listen to the entire opening, middle and ending.
2. Check white noise for harshness or tones; thunder for startling changes and believable distance; window rain for natural glass detail instead of frying/spraying texture; brown noise for bass overload; drone for distracting musical movement or beating.
3. Check mono playback and a small speaker, and check brown noise on full-range speakers. Compare MP4 sound against the FLAC master for encoding damage.
4. Record pass/revise and concrete changes in `reports/listening-review.md`. If synthetic rain is not believable, revise it or replace layers with original field recordings or documented licensed recordings; regenerate the affected preview and repeat listening.
5. Where the supplied YouTube references can be played, compare excerpts at matched perceived loudness. Record inaccessible references honestly. The browsing attempt on 2026-09-14 yielded no usable reference audio; no reference audio was downloaded, copied, sampled, or compared.

## Exact full-length production steps

Dependencies: Python 3.14, FFmpeg/FFprobe with libx264 and AAC, plus the versions in `requirements.txt`.
Full-frame verification also uses a C compiler and the local FFmpeg development libraries available through `pkg-config`.
The efficient full-video exporter requires macOS AudioToolbox (`aac_at` in FFmpeg). It encodes the title and black picture once, then encodes the entire audio continuously at a requested 160 kb/s (320 kb/s for the v1.0.0 release). AudioToolbox quality `0` is the highest setting exposed by this FFmpeg encoder ([implementation](https://github.com/FFmpeg/FFmpeg/blob/master/libavcodec/audiotoolboxenc.c)); it accepts 16-bit PCM at the AAC encoding stage, while the separate FLAC master remains 24-bit. Short previews use FFmpeg's native AAC encoder. Both paths receive the same complete-file checks.

```sh
cd /Users/rich/.openclaw/projects/sleep-videos
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
# Build the fast, exact RGB verifier for full videos:
cc -O3 -Wall -Wextra scripts/verify_black_frames.c -o .venv/bin/verify-black-frames $(pkg-config --cflags --libs libavformat libavcodec libavutil libswscale)
# Regenerate title typography after editing titles (macOS):
swift scripts/render_title_text.swift assets
# Regenerate all previews if needed:
.venv/bin/python scripts/produce.py
.venv/bin/python scripts/verify_deliveries.py
# Only after the preview listening checklist passes:
.venv/bin/python scripts/produce.py --full --listening-reviewed > reports/full-run.log 2>&1
# Alternatively, when explicitly requested with listening review still pending:
.venv/bin/python scripts/produce.py --full --render-without-listening-review > reports/full-run.log 2>&1
# Faster macOS export, with the same full-file quality checks:
.venv/bin/python scripts/produce.py --full --render-without-listening-review --efficient-video > reports/full-run.log 2>&1
.venv/bin/python scripts/verify_deliveries.py --full
# Before committing any video: re-encode from the masters (160 kb/s, <= 1 GB, full QC) and update reports/*.json:
.venv/bin/python scripts/compress_videos.py          # previews -> site/media/
.venv/bin/python scripts/compress_videos.py --full   # eight-hour videos -> videos/
```

`reports/SHA256SUMS` and `reports/full-artifact-hashes.json` describe the v1.0.0 release assets, not the compressed files.

Use `--only rain-on-window` (or another kind listed by `--help`) to regenerate one piece. Every rerun overwrites the matching generated artifacts.

The full command streams newly generated audio over 28,800 seconds per piece. It does not repeat a three-minute audio file. It writes 48 kHz/24-bit lossless masters into `masters/`, black-screen MP4s into `videos/`, and full production sheets into `reports/`. The master contains exactly 1,382,400,000 stereo sample frames and each video exactly 691,200 frames, with fades included. Both duration and decoded RGB black are asserted. Full production and exhaustive decode verification can take hours. Budget at least 70 GB of free space for five lossless masters, video outputs and temporary audio; compression and actual use vary with the source. The full renders were created on 2026-09-14. Per-file technical results are written to `reports/*-full.json` after each complete verification pass, with the collection handoff in `reports/full-summary.md`.

After rendering, inspect each full report and listen to the opening, closing, the thunder passages and their joins, and at least a representative excerpt every 30 minutes across all eight hours. At a minimum inspect 00:30:00, 01:00:00 and every subsequent half-hour through 07:30:00; inspect fade starts/ends as well. The weather sheets record native source ranges and passage order; the seed controls passage selection rather than scheduling individual strikes. A full numerical pass is not a substitute for this evaluation. Correct issues and rerender before marking a video finished.

Draft publication copy is in `youtube-metadata.md`. Use it only for verified full-length files; the previews are three minutes, not eight hours. No videos have been uploaded to YouTube. The GitHub release contains the public downloads. If a YouTube test upload is later authorized, inspect the transcoded playback and confirm duration, black image, and audio quality before publication.

## Design and measurement notes

- Original synthesis for the noise/drone tracks; documented CC0, public-domain and CC BY recordings for weather. Recording credits are embedded in weather MP4 metadata and provided with publication copy. Research and the rejected synthetic-crack prototypes are documented in [the thunder research](docs/audio/thunder-research.md).
- Constant-gain mastering aims for conservative levels of −25 to −28 LUFS, with additional headroom at −3 dBTP before AAC; final master and encoded audio must pass −2 dBTP.
- No compressor, loudness maximizer, limiter, or noise-reduction processing is applied to the delivered audio. Full renders use FFmpeg's dedicated EBU R128 analyzer with true-peak measurement; the delivered master receives a fixed gain only. Earlier preview reports used loudnorm's input measurements. The analyzer is identified in each full report.
- After the six-second branded opening, the video uses standard limited-range YUV black (16,128,128). Every decoded RGB pixel from 00:06 onward is checked for exact zero, not an approximate black threshold. Previews retain per-frame MD5 evidence; full renders use direct byte comparison in `scripts/verify_black_frames.c` to avoid hashing overhead. The first frame is separately checked to ensure the title is present.
- No binaural beats or health claims. No automatic playback on the user's speakers.
- The script's technical assertions cover samples/duration, finite audio, clipping headroom, interior silence and one-second level jumps, title presence, and black pixels in every decoded RGB video frame after 00:06. They do not guarantee absence of every perceptual defect.

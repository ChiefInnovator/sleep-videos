# Full eight-hour technical results

## Revised weather — 2026-11-02

Both weather videos were rebuilt from 48 kHz/24-bit FLAC masters using licensed real recordings and compressed with `scripts/compress_videos.py` at 160 kb/s AAC. Each is exactly 28,800 seconds, with 691,200 decoded video frames and 691,056 fully black frames after the title. Full lossless and decoded AAC checks passed; file hashes match the production sheets.

| Current full video | Master LUFS-I | Master dBTP | AAC dBTP | Largest interior 1-second AAC RMS change (dB) | Bytes |
|---|---:|---:|---:|---:|---:|
| [distant-thunder-rain](https://github.com/ChiefInnovator/sleep-videos/raw/refs/heads/main/videos/distant-thunder-rain-full.mp4) | -27.8 | -3.0 | -2.6 | 19.424 | 607,364,337 |
| [rain-on-window](https://github.com/ChiefInnovator/sleep-videos/raw/refs/heads/main/videos/rain-on-window-full.mp4) | -27.0 | -11.3 | -11.3 | 1.888 | 607,324,615 |

Thunder uses 351 consecutive real storm passages with native timing and no scene overlap or independent strike timer. Quiet recorded rain bridges joins. Window rain uses calm recorded window passages and soft fixed shaping over recorded rain. Finite source passages are reused in varied order. Sources, ranges, licenses and checksums are recorded in the JSON sheets and [source manifest](../assets/recordings/sources.json); [publication credits](../site/recording-credits.txt) are also embedded in the weather MP4 metadata.

The thunder screening limit is 20 dB for intentional natural claps; window rain retains the 3 dB steady-texture limit. All clipping, silence, duration and fade checks remain in place. The owner approved the real-thunder audition; full-mix and multi-device listening remain pending.

## Original v1.0.0 archive

The following results describe the original released audio. Its two synthesized weather tracks have been superseded by the revisions above. The release assets remain unchanged.

All five MP4s and lossless masters passed complete-file numerical verification. Each is exactly 28,800 seconds (8:00:00). Masters contain 1,382,400,000 stereo sample frames at 48 kHz/24-bit. Videos contain 691,200 frames at 1280×720 and 24 fps, with AAC encoding configured at 320 kb/s.

Each title and smaller Inventing Fire with AI logo hold for four seconds, then fade over two seconds. Every decoded RGB pixel from 00:06 onward was compared directly against zero: 691,056 completely black frames per video. Audio has a two-second opening fade and a 25-second closing fade, included in the runtime.

| Video / direct download | Duration | Master LUFS-I | Master dBTP | AAC dBTP | Largest interior 1-second AAC RMS change (dB) |
|---|---:|---:|---:|---:|---:|
| [Softened white noise](https://github.com/ChiefInnovator/sleep-videos/releases/download/v1.0.0/white-noise-full.mp4) | 8:00:00 | -25.0 | -15.0 | -15.2 | 0.208 |
| [Distant thunder and steady rain](https://github.com/ChiefInnovator/sleep-videos/releases/download/v1.0.0/distant-thunder-rain-full.mp4) | 8:00:00 | -26.0 | -15.9 | -16.0 | 0.364 |
| [Gentle rain on a window](https://github.com/ChiefInnovator/sleep-videos/releases/download/v1.0.0/rain-on-window-full.mp4) | 8:00:00 | -27.0 | -16.1 | -16.2 | 0.311 |
| [Deep brown noise](https://github.com/ChiefInnovator/sleep-videos/releases/download/v1.0.0/brown-noise-full.mp4) | 8:00:00 | -27.0 | -10.8 | -10.7 | 2.576 |
| [Deep ambient sleep drone](https://github.com/ChiefInnovator/sleep-videos/releases/download/v1.0.0/ambient-drone-full.mp4) | 8:00:00 | -28.0 | -20.2 | -20.2 | 0.140 |

All lossless and decoded AAC audio passed finite-sample, clipping-headroom, interior-silence and one-second level-change screening. Interior checks exclude the opening two seconds and closing 25 seconds. True peaks use FFmpeg EBU R128 analysis with 0.1 dB summary precision; every output is well below the -2 dBTP limit.

## Audio profiles and provenance

- **Softened white noise:** Gaussian broadband noise; 11 kHz second-order low-pass for comfort; shared center and restrained independent sides. Softened white noise, not mathematically pure white noise.
- **Distant thunder and steady rain:** Continuous filtered Gaussian rain layers at 180-8500 Hz and 800-6500 Hz, slow random intensity drift; newly synthesized band-limited thunder with irregular 29-67 second gaps, 10-19 second smooth envelopes and restrained stereo width.
- **Gentle rain on a window:** Synthetic indoor rain bed at 350-5800 Hz; randomized noise-burst droplets through a 1300-6500 Hz band, with smooth 25-95 ms envelopes and fixed gentle stereo placement; no external recordings.
- **Deep brown noise:** Leaky integration of Gaussian noise, 30 Hz high-pass for DC/subsonic control plus a 60 Hz high-pass to restrain low-bass energy surges, 1800 Hz low-pass; stable shared center and restrained independent sides. Fixed frequency shaping only, with no dynamic compression.
- **Deep ambient sleep drone:** Original sustained D/A harmonic pad at 73.416, 110, 146.832, 220 and 293.664 Hz with gentle upper partials and independent very slow phase/amplitude evolution. No binaural beat design, percussion, melody or external samples.

All audio was generated continuously from original synthesis. No preview audio was looped, and no external recordings or reference audio were copied. Rain and thunder are synthesized sound designs. Brown noise received fixed 60 Hz bass shaping after its initial full check caught rare low-frequency energy surges; its revised full master and AAC both passed the original thresholds.

## Review status

Critical listening, multi-device playback, matched-loudness reference comparisons and YouTube-transcode evaluation have not been completed. No premium-quality, health or comparative superiority claims are made. No videos have been uploaded to YouTube.

The JSON production sheets include per-second measurements, source methods, seeds, SHA-256 hashes and verification details. The thunder sheet includes every scheduled thunder event. Lossless masters remain in the production workspace's `masters/` folder. Production source is attached to the GitHub release as `sleep-soundscapes-v1.0.0-source.zip`.

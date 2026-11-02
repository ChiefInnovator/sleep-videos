# Preview technical results

All five 180-second deliveries passed numerical checks. Each master is 48 kHz/24-bit stereo. MP4s use 1280×720 at 24 fps and 320 kb/s AAC. Each video-specific title and smaller Inventing Fire with AI logo hold for four seconds and fades to black over two seconds. Every decoded video frame from 00:06 onward contains RGB (0,0,0) at every pixel. Lossless and decoded AAC audio passed finite-sample, peak, interior silence and one-second RMS-change screening. Each preview has 4,320 frames, including 4,176 completely black frames after the title.

| Sound | Master LUFS-I | Master dBTP | AAC dBTP | Master LRA (LU) | Technical checks |
|---|---:|---:|---:|---:|---|
| white-noise | -25.00 | -15.27 | -15.68 | 0.50 | Pass |
| distant-thunder-rain | -26.00 | -16.52 | -16.69 | 0.90 | Pass |
| rain-on-window | -27.00 | -17.67 | -17.73 | 0.70 | Pass |
| brown-noise | -27.0 | -12.3 | -12.3 | 1.2 | Pass |
| ambient-drone | -28.00 | -20.45 | -20.42 | 1.50 | Pass |

Critical listening, playback on multiple devices, and matched-loudness reference comparisons have not been completed. These checks cannot establish premium quality or realistic rain. See the separate full-length reports for eight-hour verification. See README.md for the listening checklist and exact full-render steps. No YouTube uploads were made.

The two-second opening fade and 25-second closing fade are excluded from interior RMS-change/silence screening. Both preview and full-length generation use these audio fade durations. Loudness range includes the effect of fades as interpreted by the measurement algorithm. The full per-second measurements, hashes, methods and provenance are in the individual JSON production sheets.

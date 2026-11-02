# Sleep Soundscapes

The marketing site and playable preview collection for **Sleep Soundscapes by Inventing Fire with AI**.

**[Visit the site](https://chiefinnovator.github.io/sleep-videos/)**

Five original three-minute previews: softened white noise, distant thunder and rain, gentle rain on a window, deep brown noise, and an ambient sleep drone. Each starts with a short title that fades to black by six seconds. The revised rain and thunder use licensed real recordings; source credits are available in `recording-credits.txt` and in each weather MP4 metadata comment.

All five eight-hour videos are available as MP4 downloads in [v1.0.0](https://github.com/ChiefInnovator/sleep-videos/releases/tag/v1.0.0). The site player offers the shorter previews, with a full-video download link for each selection. The revised weather downloads point to the current tracked full videos; the other three downloads retain the v1.0.0 release links. Weather uses finite recorded passages in varied order, with native storm timing and no artificial thunder overlap. Lossless masters are retained in the production workspace.

The full videos pass automated duration, audio-level and decoded-pixel checks; critical listening and comparisons across playback devices remain pending. No medical or sleep-outcome claims are made.

## Development

This is a static site with no build step or external JavaScript dependencies. Serve this directory with `python3 -m http.server 8000` and open `http://localhost:8000`.

`index.html` contains the page, `styles.css` the responsive design, `app.js` the preview selector, and `media/` the five MP4 previews and their title posters. Playback requires a user action. Selecting another soundscape pauses playback.

`.github/workflows/pages.yml` deploys this folder to GitHub Pages on every push to `main`. To update a preview, run `.venv/bin/python scripts/compress_videos.py --only <kind>` from the repository root. It re-encodes `media/<kind>-preview.mp4` from its FLAC master and records the hash that the `media-guard` check verifies. If the title changed, copy `assets/<kind>-title.png` into `media/` as well. Files in this folder must not use Git LFS.

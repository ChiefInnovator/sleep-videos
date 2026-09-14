# Sleep Soundscapes

The marketing site and playable preview collection for **Sleep Soundscapes by Inventing Fire with AI**.

**[Visit the site](https://chiefinnovator.github.io/sleep-videos/)**

Five original three-minute previews: softened white noise, distant thunder and rain, gentle rain on a window, deep brown noise, and an ambient sleep drone. Each starts with a short title that fades to black by six seconds. The rain and thunder are synthesized sound designs, not field recordings.

All five eight-hour videos are available as MP4 downloads in [v1.0.0](https://github.com/ChiefInnovator/sleep-videos/releases/tag/v1.0.0). The site player offers the shorter previews, with a full-video download link for each selection. Every full track is freshly synthesized over eight hours, rather than repeating its preview. Lossless masters are retained in the production workspace.

The full videos pass automated duration, audio-level and decoded-pixel checks; critical listening and comparisons across playback devices remain pending. No medical or sleep-outcome claims are made.

## Development

This is a static site with no build step or external JavaScript dependencies. Serve this directory with `python3 -m http.server 8000` and open `http://localhost:8000`.

`index.html` contains the page, `styles.css` the responsive design, `app.js` the preview selector, and `media/` the five MP4 previews and their title posters. Playback requires a user action. Selecting another soundscape pauses playback.

GitHub Pages publishes the root of `main`. To update a preview, replace its MP4 and matching poster in `media/`, then push the change.

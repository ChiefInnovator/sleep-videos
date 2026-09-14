# Sleep Soundscapes

The marketing site and playable preview collection for **Sleep Soundscapes by Inventing Fire with AI**.

**[Visit the site](https://chiefinnovator.github.io/sleep-videos/)**

Five original three-minute previews: softened white noise, distant thunder and rain, gentle rain on a window, deep brown noise, and an ambient sleep drone. Each starts with a short title that fades to black by six seconds. The rain and thunder are synthesized sound designs, not field recordings.

The eight-hour editions are planned and are not yet available. These previews are not medical treatments and carry no claims about sleep outcomes.

## Development

This is a static site with no build step or external JavaScript dependencies. Serve this directory with `python3 -m http.server 8000` and open `http://localhost:8000`.

`index.html` contains the page, `styles.css` the responsive design, `app.js` the preview selector, and `media/` the five MP4 previews and their title posters. Playback requires a user action. Selecting another soundscape pauses playback.

GitHub Pages publishes the root of `main`. To update a preview, replace its MP4 and matching poster in `media/`, then push the change.

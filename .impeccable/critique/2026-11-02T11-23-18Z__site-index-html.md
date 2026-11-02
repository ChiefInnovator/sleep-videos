---
target: Sleep Soundscapes landing page
total_score: 20
max_score: 32
na_heuristics: 7,10
p0_count: 0
p1_count: 2
target_identity: "file:/Users/rich/.openclaw/projects/sleep-videos/site/index.html"
target_fingerprint: "sha256:ed9b6e3e3c7514dfc5a263f1182c982348886e8522f25af5c971be5ebb63c120"
target_path: /Users/rich/.openclaw/projects/sleep-videos/site/index.html
timestamp: 2026-11-02T11-23-18Z
slug: site-index-html
---
# Critique: site/index.html (Sleep Soundscapes landing page)

Method: two isolated sub-agents (A design review, B detector and browser overlay). Mode: Persuade.

## Design specificity

The page is mostly specific to this product. The eclipse motif, "BLACK SCREEN AFTER 00:06", the title posters and the moss and ember palette all come from how the videos actually behave. It weakens on mobile: the eclipse is hidden, and the strongest verified differentiator (continuous eight-hour synthesis with no loops or samples) never appears.

## Heuristics (20/32; #7 and #10 n/a)

| # | Heuristic | Score |
|---|---|---|
| 1 | Visibility of system status | 2 |
| 2 | Match with the real world | 3 |
| 3 | User control and freedom | 3 |
| 4 | Consistency and standards | 2 |
| 5 | Error prevention | 2 |
| 6 | Recognition rather than recall | 3 |
| 8 | Aesthetic and minimalist design | 3 |
| 9 | Error recovery | 2 |

## Priority issues

1. [P1] The next step to the full video is a 12px link with the same weight as "Download preview", and no size is shown. Make it a single primary button with the size, and demote the preview link.
2. [P1] On mobile, selection and playback are about 470px apart. Bring the player into view when a track is selected.
3. [P2] Amber is used on six elements in the first viewport, which breaks the One Light Rule. Mute the eyebrows and "WITH AI".
4. [P2] The eclipse art is hidden at 700px and below. Show a small version.
5. [P2] The verified differentiator is absent. Add one factual sentence to 03 / ORIGIN, linked to the production report.

## Detector findings (B)

- tiny-text / undersized-ui-text: 9–10px eyebrows, collection note and art caption on mobile.
- Hit targets under 24px tall: nav and footer links.
- italic-serif-display: the hero and closing `em`.
- hero-eyebrow-chip and kicker-above-heading (×3).
- numbered-section-labels.
- dark-glow: the eclipse shadow.
- side-tab: the selected track's inset edge.
- design-system-color/font-size advisories.
- Contrast passes everywhere (muted text 6.09–8.47:1).

## Technical

- The error message says the links are "below"; they are above it.
- `.principles h3` uses the sans, which breaks the Two Voices Rule.
- An on-page anchor uses the external ↗ arrow.
- No og:image.
- Performance is good: previews are 3.6–4.1 MB with preload none, and there is no third-party JS.

## Persona red flags

- Bedtime phone listener: tapping a track does nothing audible, and the full video is a small, unsized link to GitHub.
- First-timer: "GitHub" in the navigation means nothing to them.

## Questions

- Should GitHub stay in the main navigation once YouTube exists?
- Should picking a sound start playback?

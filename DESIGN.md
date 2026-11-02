---
name: Sleep Soundscapes
description: Five original eight-hour soundscapes by Inventing Fire with AI. A little sound, a little less world.
colors:
  night-moss: "#101211"
  moss-surface: "#181b18"
  track-rail: "#141713"
  approach-band: "#191d17"
  track-hover: "#22281e"
  track-selected: "#2b3025"
  pale-linen: "#eeede6"
  lichen-gray: "#adafa6"
  hairline-moss: "#343931"
  ember-amber: "#efb477"
  ember-amber-hover: "#f4c593"
  ember-ink: "#21170f"
  ember-warning: "#f1bb93"
  pure-black: "#000000"
typography:
  display:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "clamp(66px, 7.5vw, 104px)"
    fontWeight: 400
    lineHeight: 1.01
    letterSpacing: "-0.055em"
  headline:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "clamp(38px, 4.2vw, 58px)"
    fontWeight: 400
    lineHeight: 1.12
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "29px"
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
  body-lead:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "22px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "-0.025em"
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "0.16em"
rounded:
  hairline: "3px"
  panel: "6px"
  full: "50%"
spacing:
  gutter-mobile: "20px"
  gutter-tablet: "24px"
  gutter-desktop: "48px"
  section: "95px"
  container: "1200px"
components:
  button-primary:
    backgroundColor: "{colors.ember-amber}"
    textColor: "{colors.ember-ink}"
    rounded: "{rounded.hairline}"
    padding: "14px 22px"
  button-primary-hover:
    backgroundColor: "{colors.ember-amber-hover}"
    textColor: "{colors.ember-ink}"
  track-item:
    backgroundColor: "{colors.track-rail}"
    textColor: "{colors.pale-linen}"
    padding: "25px 22px"
    height: "100px"
  track-item-hover:
    backgroundColor: "{colors.track-hover}"
  track-item-selected:
    backgroundColor: "{colors.track-selected}"
  listening-room:
    backgroundColor: "{colors.moss-surface}"
    rounded: "{rounded.panel}"
  video-frame:
    backgroundColor: "{colors.pure-black}"
    rounded: "{rounded.hairline}"
---

# Design System: Sleep Soundscapes

## Overview

**Creative North Star: The Slow Eclipse.** Each video holds a title for four seconds, fades it out over two, and then stays black. The site follows the same arc. A single warm light, ember amber, sits on a near-black, faintly green night. Large serif headlines are quiet but present, and everything else recedes into thin rules and muted text. The page should feel like a lamp being turned down, not like a product being sold loudly.

The mood is calm, nocturnal, editorial and unhurried. The look works in low light and in a dark bedroom at minimum brightness. It avoids neon "sleep app" gradients, starfield clichés, glowing purple, and stock photos of people asleep.

**The One Light Rule.** Ember amber (#efb477) is the only chromatic light on the page. It marks what to act on or notice: the primary button, the selected track, eyebrows, numbering, and focus rings. If two things compete in amber, one of them is wrong.

## Colors

The palette is a dark, slightly green-tinted night ("moss") lit by one warm ember.

- **Night Moss (#101211):** the page background. It is green-black rather than pure black, so the video's true black still reads as a deeper void.
- **Moss Surface (#181b18):** the listening-room panel.
- **Track Rail (#141713):** the track list column, set slightly below the surface.
- **Approach Band (#191d17):** the full-bleed "approach" section band.
- **Track Hover (#22281e) / Track Selected (#2b3025):** tonal steps up for interactive rows. The selected row also carries a 3px amber inset edge.
- **Pale Linen (#eeede6):** primary text. Warm off-white, never pure white.
- **Lichen Gray (#adafa6):** secondary text, navigation and metadata.
- **Hairline Moss (#343931):** every divider and border.
- **Ember Amber (#efb477) / hover (#f4c593):** the accent. **Ember Ink (#21170f)** is the text color on amber fills.
- **Ember Warning (#f1bb93):** the error message. A softened amber rather than red, so an error doesn't jolt.
- **Pure Black (#000000):** reserved for the video frame.

**The Deeper Black Rule.** Only the video is pure black. Every other surface keeps the moss tint, so the player reads as the darkest, quietest object on the page.

## Typography

The type pairs a serif for feeling with a system sans for information.

- **Display (Georgia, 66–104px fluid, 400, -0.055em):** the hero headline. The emphasized phrase is set in `<em>` with no italic, colored amber ("fade out.").
- **Headline (Georgia, 38–58px fluid, -0.035em):** section headings. The closing section scales up to 48–76px.
- **Title (Georgia 29px):** the name of the selected track in the player.
- **Body (system sans 16px/1.6)** and **Body Lead (22px)** for the hero's one-line promise.
- **Label (system sans 10–12px, 600, +0.12–0.16em tracking, uppercase copy):** eyebrows, the collection note and player labels. Track numbers and durations use `tabular-nums`.

**The Two Voices Rule.** Serif carries emotion (headlines, track title). Sans carries facts (descriptions, durations, links). Never set metadata in the serif, and never set a headline in the sans.

## Layout

- A single centered container, `min(1200px, 100% − 96px)`. Gutters are 48px per side on desktop, 24px below 950px, and 20px below 700px.
- The hero is a two-column grid (1.2fr text, 1fr art). It collapses to one column below 700px, where the eclipse art is hidden.
- The listening room is a two-column panel (1fr track list, 1.35fr player). It stacks below 700px, with the player under the list.
- Vertical rhythm is generous, at 85–95px section padding on desktop and 50–58px on mobile. Sections are separated by full-width hairlines, not by changes of background (the approach band is the one exception).

**The Long Exhale Rule.** Space is the main way content is grouped. Prefer more padding and a hairline over a box, a card or a shadow.

## Elevation & Depth

The page is flat. Depth comes from tonal steps between the moss surfaces and from hairline borders, not from drop shadows. The only shadows belong to the illustrative eclipse (ambient glow and inner rim light), and they are part of the art, not of the UI. The selected track uses an inset amber edge, not a lift.

## Shapes

Corners are nearly square: 3px on buttons and the video, 6px on the listening-room panel. Circles appear only in the eclipse motif (eclipse, orbits) and the eyebrow dot. Never use pill-shaped buttons or rounded cards.

## Components

- **Primary button:** an amber fill with Ember Ink text, 3px radius, 14×22px padding, and a wide 40px gap before its arrow glyph. Hover lightens to #f4c593. There is one primary button per view.
- **Track item:** a full-width row button with a number, name and short description, and a duration on the right. It uses `aria-pressed` for selection: the selected row gets a tonal background plus a 3px inset amber edge. The minimum height is 100px on desktop and 82px on mobile, so it is easy to tap in bed.
- **Player panel:** a label row (`PREVIEW / 01`, `03:00`), a 16:9 black video with native controls and `preload="none"`, a serif title with a muted description, and a footer of amber text links (full video, preview download). The error text is Ember Warning with `role="alert"`.
- **Text link:** amber, with a 5px underline offset and an arrow glyph spaced 8–20px away.
- **Focus:** a 2px amber outline with a 6px offset on links, buttons and the video.
- **Eclipse art:** a CSS-only radial-gradient disc with two hairline orbits, rotated −28°, decorative and `aria-hidden`.

## Do's and Don'ts

- **Do** keep amber as the single light source, and keep pure black for the video only.
- **Do** keep every playback behind a tap. Nothing autoplays, and switching tracks pauses playback.
- **Do** honor `prefers-reduced-motion` for any motion added later. Motion, if any, should be slow fades, never bounces.
- **Don't** add bright whites, saturated blues or purples, gradients behind text, glassmorphism, or glows on UI elements.
- **Don't** add shadows or rounded cards to create hierarchy. Use space and hairlines.
- **Don't** add imagery of sleeping people, moons with faces, or starfields. The eclipse is the motif.
- **Don't** set body or metadata copy in the serif, or headlines in the sans.

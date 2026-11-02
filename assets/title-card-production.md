# Inventing Fire with AI title card

Created with the built-in image generation tool using the existing brand image at `/Users/rich/.openclaw/projects/inventingfirewithai_skills/docs/assets/images/inventing-fire-brand.png` as the visual reference. Saved project asset: `assets/inventing-fire-title.png`. The supplied brand artwork was visually inspected before generation. This is an AI-generated adaptation of the existing mark, not a pixel-identical placement of the source logo.

The card is shown for four seconds and fades to black over two seconds. At 24 fps, frames 0–143 contain the opening; frame 144 and all subsequent frames must decode to exact RGB black. It is fitted to the existing 1280×720 videos. No sound effect or extra audio is added. The opening occupies the first six seconds of the existing track and does not extend runtime.

## Generation prompt

Use case: compositing. Create a finished 16:9 widescreen title card for the opening six seconds of a premium sleep-audio video. Reference image is the user's existing Inventing Fire with AI brand logo; preserve its distinctive orange/gold three-tongue flame silhouette and brand identity faithfully. Pure black background, restrained warm gold/orange flame centered above a clean, beautifully spaced wordmark, plenty of black negative space. Exact text: "INVENTING FIRE" on one line and "WITH AI" smaller underneath, all letters readable on black in warm gold/off-white. Center the whole lockup. Flame around 25 percent of canvas height; complete composition within the central 60 percent width and 65 percent height. Flat polished brand artwork, no photorealistic fire, no scenery, no starfields, no additional slogans, no borders, no shadows, no extra text. Output 1920x1080 or equivalent exact 16:9 image. Intended as a calm static video opening that fades to black.

## Video-specific opening revision

Each opening now features the matching title from `review.html` in warm off-white at 48 px on a 1280×720 black canvas. `scripts/render_title_text.swift` renders the exact typography using CoreText. FFmpeg scales the existing brand artwork to 400×225 and places it below the title at (440, 380), reducing its width to 31.25% of the former full-frame treatment. The original brand asset is retained. Both elements hold for four seconds and fade together over two seconds. `assets/*-title.png` posters are extracted from the rebuilt video opening frames.

---
name: motion-studio
description: House rules for building, checking and scheduling motion videos for every one of Greg's brands (The Campbell-Maric Group, SecureMyOffer, The Canadian Close, The-Me-Dia, Big Stuff and any new one). Use whenever a script becomes a rendered video, Reel, Short or Story; when captions, covers, file names or Metricool scheduling for a video come up; or for the cut-paper and claymation series styles. Brand-specific script skills (tcmg-video, smo-video, smo-avatar-script, static-to-reel and others) decide what the video says; this skill decides how it is built and shipped.
---

# Motion Studio

These are the shared rules for every motion video, whatever the brand. The full guide and the code live in the GitHub repo `bigmachine1974/1sttask`, in `motion/README.md`. Read that file first when the repo is available.

## Captions (all brands)
- Centre them at the bottom: a dark bar with bold sans-serif body text, the key phrase in the brand's accent colour (`*phrase*`), two lines at most (`|` breaks the line).
- Centre the one line of fine print above the bar too (source, plus the brand's legal or brokerage line).
- Time captions from the voiceover, not by hand: run `motion/common/autocaps.py <video folder>`. Write each caption line to match the script line it covers.

## Styles
- **Flat motion graphics:** the default explainer look, as in the Oct 2026 TCMG explainers.
- **Cut paper:** torn paper, drop shadows, paper grain, animated on twos (12 poses a second) with edges that re-tear each pose. Fast to render. Reference: `motion/tcmg-paper-test/`.
- **Clay:** Blender claymation with matte clay, thumbprints, soft bevels, a tabletop set, shallow focus, on twos with a small per-pose jitter.
  - Always approve a still before animating.
  - Reference: `motion/tcmg-clay-test/make_clay.py`.
  - Slow without a graphics card (about 3 hours for 6 s in the cloud), so use it for hero pieces or render on the Mac.
- Any style takes the brand's colours and fonts from its brand profile.

## Before anything is scheduled
1. Watch a review render. Check fonts, caption sync and anything clipped at the edges.
2. Choose the Instagram and Facebook cover: a title frame, never blank or mid-animation (usually 2–3 s in). Set it in Metricool as `videoCoverMilliseconds`.
3. Name the file `<brand>-<topic>-<ratio>.mp4` (for example `tcmg-test-the-commute-9x16.mp4` or `smo-sold-isnt-closed-9x16.mp4`) and store it in the brand's Dropbox video folder.
4. Schedule from Dropbox: make a temporary download link, pass it as the post's media, and confirm the copy Metricool stored is the same file size. Stories reuse the Reel's stored file.
5. When replacing a video in a scheduled post, change only the media. Keep the caption, title, cover, time and AI label.

## Brand profiles
Each brand supplies its colours, fonts, fine-print line, end card, contact line and Dropbox folder. Profiles are kept in `motion/README.md`. When a brand without a profile makes its first video, ask for these details, then add a profile.

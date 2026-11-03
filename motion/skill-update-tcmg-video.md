<!-- Paste everything below this line at the end of the tcmg-video skill (claude.ai → Settings → Capabilities → Skills → tcmg-video → edit SKILL.md). Delete this comment. -->

## Motion video build rules (added Nov 2026)

These apply whenever a TCMG script becomes a rendered motion video. The full guide and the code are in the GitHub repo `bigmachine1974/1sttask`, in `motion/README.md`. Read it first when the repo is available.

**Captions**
- Centred at the bottom: a dark bar, white Manrope 700 at 38 px, with brass on the key phrase (`*phrase*`). Two lines at most, with `|` for the break.
- The one line of fine print above the bar (source plus "The Campbell-Maric Group · eXp Realty, Brokerage") is centred too. Headlines stay left-aligned.
- Time the captions from the voiceover, not by hand: run `motion/common/autocaps.py` on the video folder. Write each caption line to match the script line it covers, so the timing script can line them up.

**Before anything is scheduled**
- Render a review copy and check fonts (Mansfield headlines, Manrope body), caption sync and anything clipped at the edges.
- Choose the Instagram cover: a title frame, never blank or mid-animation (usually 2–3 s in). Set it in Metricool as `videoCoverMilliseconds`.
- Name the file `tcmg-<topic>-9x16.mp4` and store it in Dropbox under `/TCMG/Videos/`.
- Schedule from Dropbox: make a temporary download link, pass it as the post's media, and confirm the copy Metricool stored is the same file size. Stories reuse the Reel's stored file.
- When replacing a video in a scheduled post, change only the media. Keep the caption, title, cover, time and AI label as they are.

**Series styles**
- **Paper Ottawa** (cut paper): one neighbourhood per episode (Orléans first). Torn paper with drop shadows, animated on twos, in TCMG colours. The reference scene is `motion/tcmg-paper-test/`.
- **Clay series** (working name Small Moves): buying and selling moments, built in Blender as claymation.
  - Always approve a still before animating.
  - Animated on twos with a small per-pose jitter. The reference scene is `motion/tcmg-clay-test/make_clay.py`.
  - Slow to render without a graphics card (about 3 hours for 6 s in the cloud), so plan clay as occasional hero pieces or render on the Mac.

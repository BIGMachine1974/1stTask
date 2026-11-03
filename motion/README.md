# TCMG video formats

How The Campbell-Maric Group's motion videos are built, checked and posted. Read this before building or changing any video in `motion/`.

## The pipeline

Every video is one `index.html` that draws each frame on a 1080×1920 canvas, captured frame by frame with Playwright and encoded with FFmpeg.

- `motion/common/tcmg-motion.js` is the shared kit: brand colours, springs, captions, fine print and the end card.
- A video page sets `window.DUR`, `window.CAPS`, `window.END` and `window.scenes(t)`.
- `node <video>/render.js video` renders the picture. `motion/common/render_all.sh` shows how to add the mix (`mix.wav`) and make the 4:5 crop (`crop=1080:1350:0:285`).
- Review renders go in `<video>/REVIEW/`, numbered and versioned: `07-tcmg-commute-test-the-commute-v6-centred-captions-9x16.mp4`.

**Fonts:** Mansfield is licensed, so it's git-ignored. Download it from Dropbox `/Mansfield Font/` into `<video>/assets/` as `Mansfield-Semi-Bold.ttf` and `Mansfield-Extra-Bold.ttf`. Manrope is in the repo.

## Captions

- **Centred** at the bottom (the default since Nov 2026): the dark bar, its lines, and the single line of fine print above it. A page can set `window.CAP_CENTER=false` for the old left-aligned look. Headlines stay left-aligned.
- Wrap emphasis in `*brass*`, and use `|` for a line break. Two lines at most.
- **Timing is automatic:**
  ```
  python3 motion/common/autocaps.py motion/<video>            # compare with the current timings
  python3 motion/common/autocaps.py motion/<video> --write    # write them into index.html
  ```
  - It keeps your caption text and replaces only the times, using faster-whisper word timings from `vo.mp3`. It reads spoken numbers ("twenty" = "20") and checks the audio for where each line really starts.
  - On the three Oct 2026 videos, it landed within 0.15 s of hand timing on every line, most within 0.05 s.
  - It also saves `words.json`, per-word timing for word-by-word highlighting.
  - It needs `pip install faster-whisper` and network access to huggingface.co for the model download.

## Series styles

### Paper Ottawa (cut paper): places

One neighbourhood per episode, starting with Orléans. Reference scene: `motion/tcmg-paper-test/`.

- Torn edges, drop shadows and paper grain.
- Animated **on twos** (12 poses a second), with edges re-tearing on every pose.
- Uses TCMG colours and fonts. Renders in about a minute.

### Clay (Blender claymation): moments

Small stories from buying and selling. Working name: Small Moves. Reference scene: `motion/tcmg-clay-test/make_clay.py`.

- Matte clay with thumbprints, soft bevels, lumps and a tabletop set.
- Warm key light and shallow depth of field.
- On twos, with a small per-pose "boil" jitter.

How to render:
- **Always render a still first** (`-- stills 5.5 --res 360 --samples 12`). Check it looks like clay, not plastic, before animating.
- Render poses with `-- poses`. Finished poses are skipped, so a stopped render resumes. Then run `render.sh` to hold each pose 2 frames and add music.
- **Cost:** no graphics card in cloud sessions, so it's Cycles on the CPU, about 2–3 minutes a pose at 540×960. A 6 s clip takes about 3 hours.
- Use clay for occasional hero pieces, or render on the Mac with the Blender connector.

## Before posting

1. **Watch the review render.** Check fonts, caption sync and anything clipped at the edges.
2. **Choose the Instagram cover.** Use a title frame, never a blank or mid-animation frame. Set it in Metricool with `videoCoverMilliseconds`, or with `videoThumbnailUrl` for a custom image.
   - The Oct 2026 explainers use 2.2–2.7 s.
   - Check the frame with `ffmpeg -ss <s> -i video.mp4 -frames:v 1 cover.png`.
3. **Name files** `tcmg-<topic>-9x16.mp4`. Store them in Dropbox under `/TCMG/Videos/` (explainers: `/TCMG/Videos/New Format Explainer Videos/`).
4. **Get the video into Metricool.** Make a Dropbox temporary download link for the file and pass it as `media`. Metricool copies it to its own storage.
   - Confirm the stored file is the same size (`curl -sI <static.metricool.com url>`).
   - Stories can reuse the Reel's stored URL, so there's no second upload.
5. **Replacing a scheduled video:** update the post with the full original content. Change only `media`, and keep the caption, title, cover, time and `isAiGenerated`.

## Brand rules that show up in every video

- Fine print carries the source and "The Campbell-Maric Group · eXp Realty, Brokerage".
- The end card is the TCMG lockup on carbon, with yourhomeinottawa.ca and 613-799-9022.
- Colours: carbon `#121411`, parchment `#f1efe8`, brass `#c2a56a` (light `#d8c08f`, dark `#725b2f`), moss `#59644d`.

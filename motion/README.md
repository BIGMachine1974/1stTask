# Motion Studio

The shared system for building, checking and posting motion videos for every brand: The Campbell-Maric Group, SecureMyOffer, The Canadian Close, The-Me-Dia, Big Stuff and any new one. Read this before building or changing any video in `motion/`.

The rules and tools below apply to every brand. Only the **brand profile** (colours, fonts, fine print, end card, folders) changes.

## The pipeline

Every video is one `index.html` that draws each frame on a 1080×1920 canvas, captured frame by frame with Playwright and encoded with FFmpeg.

- A **brand kit** in `motion/common/` holds the colours, captions, fine print and end card. `tcmg-motion.js` is the TCMG kit. A new brand gets its own kit, copied from it, with that brand's profile.
- A video page loads its brand kit and sets `window.DUR`, `window.CAPS`, `window.END` and `window.scenes(t)`.
- `node <video>/render.js video` renders the picture. `motion/common/render_all.sh` shows how to add the mix (`mix.wav`) and make the 4:5 crop (`crop=1080:1350:0:285`).
- Review renders go in `<video>/REVIEW/`, numbered and versioned: `07-tcmg-commute-test-the-commute-v6-centred-captions-9x16.mp4`.
- Licensed fonts are git-ignored. Download them from Dropbox (Mansfield: `/Mansfield Font/`) into `<video>/assets/`.

## Captions (all brands)

- **Centred** at the bottom: the dark bar, its lines, and the single line of fine print above it. A page can set `window.CAP_CENTER=false` for a left-aligned look. Headlines stay left-aligned.
- Wrap emphasis in `*accent*`, in the brand's accent colour. Use `|` for a line break. Two lines at most.
- **Timing is automatic:**
  ```
  python3 motion/common/autocaps.py motion/<video>            # compare with the current timings
  python3 motion/common/autocaps.py motion/<video> --write    # write them into index.html
  ```
  - It keeps the caption text and replaces only the times, using faster-whisper word timings from `vo.mp3`. It reads spoken numbers ("twenty" = "20") and checks the audio for where each line really starts.
  - Tested on three videos: every line landed within 0.15 s of hand timing, most within 0.05 s.
  - It also saves `words.json`, per-word timing for word-by-word highlighting.
  - It needs `pip install faster-whisper` and network access to huggingface.co for the model download.

## Styles (any brand)

### Flat motion graphics
The default explainer look. Examples: the TCMG cost, commute and schools videos.

### Cut paper
Reference scene: `motion/tcmg-paper-test/`.
- Torn edges, drop shadows and paper grain.
- Animated **on twos** (12 poses a second), with edges re-tearing on every pose.
- Renders in about a minute.

### Clay (Blender claymation)
Reference scene: `motion/tcmg-clay-test/make_clay.py`.
- Matte clay with thumbprints, soft bevels, lumps and a tabletop set.
- Warm key light and shallow depth of field.
- On twos, with a small per-pose "boil" jitter.

How to render:
- **Always render a still first** (`-- stills 5.5 --res 360 --samples 12`). Check it looks like clay, not plastic, before animating.
- Render poses with `-- poses`. Finished poses are skipped, so a stopped render resumes. Then run `render.sh` to hold each pose 2 frames and add music.
- **Cost:** no graphics card in cloud sessions, so it's Cycles on the CPU, about 2–3 minutes a pose at 540×960. A 6 s clip takes about 3 hours.
- Use clay for hero pieces, or render on the Mac with the Blender connector.

## Series

| Series | Brand | Style | Idea |
|---|---|---|---|
| Paper Ottawa | TCMG | Cut paper | One neighbourhood per episode, starting with Orléans |
| Small Moves (working name) | TCMG | Clay | Buying and selling moments |

New series for other brands slot in here.

## Before posting (all brands)

1. **Watch the review render.** Check fonts, caption sync and anything clipped at the edges.
2. **Choose the Instagram and Facebook cover.** Use a title frame, never a blank or mid-animation frame. Set it in Metricool with `videoCoverMilliseconds`, or with `videoThumbnailUrl` for a custom image.
   - Usually 2–3 s in.
   - Check the frame with `ffmpeg -ss <s> -i video.mp4 -frames:v 1 cover.png`.
3. **Name files** `<brand>-<topic>-<ratio>.mp4`, for example `tcmg-test-the-commute-9x16.mp4` or `smo-sold-isnt-closed-9x16.mp4`. Store them in the brand's Dropbox video folder (see the profiles).
4. **Get the video into Metricool.** Make a Dropbox temporary download link for the file and pass it as `media`. Metricool copies it to its own storage.
   - Confirm the stored file is the same size (`curl -sI <static.metricool.com url>`).
   - Stories can reuse the Reel's stored URL, so there's no second upload.
5. **Replacing a scheduled video:** update the post with the full original content. Change only `media`, and keep the caption, title, cover, time and `isAiGenerated`.

## Brand profiles

Each profile lists: file prefix, colours, fonts, fine-print line, end card, contact line, Dropbox video folder and Metricool brand.

### The Campbell-Maric Group (TCMG)
- **Prefix:** `tcmg-`
- **Kit:** `motion/common/tcmg-motion.js`
- **Colours:** carbon `#121411`, parchment `#f1efe8`, brass `#c2a56a` (light `#d8c08f`, dark `#725b2f`), moss `#59644d`.
- **Fonts:** Mansfield (headlines), Manrope (body and captions).
- **Fine print:** source, plus "The Campbell-Maric Group · eXp Realty, Brokerage".
- **End card:** TCMG lockup on carbon, yourhomeinottawa.ca, 613-799-9022.
- **Dropbox:** `/TCMG/Videos/` (explainers: `/TCMG/Videos/New Format Explainer Videos/`).
- **Metricool:** "The Campbell-Maric Group", id 6009575.

### SecureMyOffer (SMO)
- **Prefix:** `smo-`
- **Metricool:** "Securemyoffer", id 6009566.
- **Colours, fonts, fine print, end card and Dropbox folder:** add when the first SMO video is built. Claims still go through smo-compliance.

### The Canadian Close, The-Me-Dia, Big Stuff and others
- Add a profile when each brand makes its first video.
- **Metricool ids:** bigstuff_official 6932042, The-Me-Dia 7336118.

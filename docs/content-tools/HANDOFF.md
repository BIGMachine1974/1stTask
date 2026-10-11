# Content tools handoff: diagram-design + motion-broll

Last updated 2026-10-11. Written for Greg, and for any Claude session picking this up.

## What's set up

Two open-source Claude skills are vendored into `.claude/skills/` in this repo. Any Claude Code
session that opens this repo (cloud or Mac) loads them automatically.

| Skill | What it does | Source (MIT) | Pinned commit |
|---|---|---|---|
| `diagram-design` | Branded diagrams (44 types) as one HTML/SVG file, PNG export | github.com/cathrynlavery/diagram-design | `7a2e221` (2026-10-10) |
| `motion-broll` | Animated cutaways / panels timed to the words in a talking-head video | github.com/Barty-Bart/motion-graphics | `83355bb` (2026-10-05) |

Both were read before vendoring: no telemetry, no accounts, no hidden network calls. diagram-design
loads Google Fonts in its output; motion-broll installs Playwright + Chromium into a local `motion/`
folder on first run (git-ignored).

To update either skill later, re-copy the folder from the source repo and bump the commit above.

## Still to do (Greg)

1. **Merge this branch** (`claude/add-content-skills`) into the default branch
   (`claude/multi-agent-planning-CYzCU`). New cloud sessions only see the skills after that.
2. **Allow Descript downloads in the cloud environment.** On a computer, go to claude.ai/code, open
   the environment menu in the session title bar → Edit → Network access, and add
   `share.descript.com` (or pick a broader level). The first run may reveal a second Descript file
   host to add. ffmpeg is already installed in the cloud image; no setup script is needed.

## Test 1: diagram-design (done)

`docs/content-tools/smo-buyer-default.html` / `.png`: "When a buyer walks away" flowchart,
no coverage vs. with SMO. Passed the skill's self-check and geometry checks.

- **SMO skin** (onboarded from securemyoffer.com): paper `#f7f4ee`, ink `#1a1b1f`, muted `#5c5448`,
  accent `#7d5f27` (brand gold `#cca565` darkened to 5.4:1 contrast; raw gold used only as a
  decorative rule). Node font Montserrat (Articulat CF is a paid Adobe font), titles Instrument Serif,
  labels Geist Mono.
- **Facts** came only from the smo-quoting skill and the live site. No tier names, prices, or
  "guarantee" language.
- **Not yet done:** run it through `smo-compliance` before posting. Offer to save the skin as a named
  profile (see the skill's `references/profiles.md`) so later diagrams skip onboarding.

## Test 2: motion-broll (next)

- **Clip:** Descript project "NEW SMO Short form" (`d57d1eb7-1ff2-4743-b7c4-4dfc77b54053`),
  composition "The Deposit Protects You?" (`20ecfba0-de08-415d-82c0-9d312922adcb`), 29s, vertical
  talking head with captions. Public share: https://share.descript.com/view/p9YHnMzIly8
- **Transcript:** pull it with the Descript connector (`export_transcript`, format `srt`).
- **Video:** blocked in the cloud until step 2 above is done. Otherwise Greg exports the MP4 and
  attaches it, or runs it on the Mac.
- **Do not republish the composition** to get a download link: that overwrites the public share page.
- **Expected output:** 2–3 full-frame cutaways (the frame has no empty space for side panels):
  1. ~0:07–0:16 "trust account… consent or a court order… six to 18 months" → short timeline
  2. ~0:21–0:23 "The deposit is the legal dispute" → text card
  3. ~0:23–0:27 "pays the seller directly" → closing card
- Every on-screen line is a new written claim, so run it through `smo-compliance`.
- Hand back the clips + preview. Greg drops them into a **copy** of the composition in Descript; the
  original stays as is.
- **Cloud note:** Chromium is preinstalled at `/opt/pw-browsers/chromium`. If motion-broll's
  `setup.sh` fails on `npx playwright install chromium`, point Playwright at that path instead of
  downloading.

## Decisions so far

- B-roll is **not** for every video. Talking head + captions stays the default; test cutaways on
  explainer-style clips and compare retention (Metricool) against similar clips without them.
- A cutaway version is a refresh of the same video: fine to repost or A/B test as a Seller Ad. Keep
  the original live.
- Repos reviewed and passed on: **claude-mem** (opt-out telemetry, paid cloud summarizer, hooks on
  every tool call), **HyperFrames Student Kit** (overlaps Descript), **Remotion** (paid licence above
  3 employees). **ppt-master** is still worth a test for market-snapshot decks now that Faces.app is
  out. Use your own Claude account, not the sponsor "API relay" services in its README.
  **claude-motion-design** (howseen-ai) is the pick for short branded promos cut to music.

# Automate AI Consulting: takeaways for The-Me-Dia

Source: @automateaiconsulting (23.1K subs, ~1M total views). These notes cover their last 50 Shorts (Mar to Sep 2026). I ran a full Sandcastles analysis on the 10 most relevant ones. The channel only posts Shorts: 35 to 45 second "here's the stack" tutorials. The actual repo links sit in pinned comments, which I couldn't open from here (YouTube is blocked in this environment).

## 1. Workflows worth adopting

### A. Claude to Canva carousels (6x outlier, 46K views)
Claude → Customize → Connectors → connect Canva. In Claude Design, set the project to high fidelity and upload 3 to 5 reference screenshots as a mood board. Then ask it to build a carousel template in Canva. Answer its clarifying questions and export. The design opens in Canva and stays fully editable.
- **For us:** this fits The-Me-Dia carousels and client personal-brand carousels well. The Canva connector is already attached to this account. Seed it with the brand tokens (ink `#1a211d`, gold `#c6a679`, cream `#fbf9f2`) and past posts as the mood board. That way every carousel comes out on-brand and editable instead of a flat PNG.

### B. "$10K website" stack (33x outlier, 261K views: the channel's biggest hit by far)
1. Claude Code
2. Framer Motion (animation library)
3. "UI/UX Pro Max" Claude skill
4. 21st.dev components (copy the prompt line into Claude Code)

Polish layer from "5 Claude plugins that make AI websites look premium":
- **Awesome Design**: a design system (type, spacing, colour, buttons)
- **Vercel Web Design Guidelines**: audits code against Vercel's standards
- **Taste Skill**: premium references so the UI doesn't look generic
- **Playwright**: Claude opens a browser, screenshots its own build and catches breakage
- **Image-to-code**: mockup to working front end
- **Apple design-language skill**: audits an existing site for the small details that make it "feel cheap"

**For us:** client landing pages, link-in-bio pages and discovery pages (`tools/questionnaire`, `dj-discovery`). The point that matters most is that you don't prompt "make it premium". You give Claude a design rulebook, then let it check its own render with Playwright. A The-Me-Dia design-system skill built on our tokens would do the same job.

### C. Apple-style scroll animation (22K views, 6% engagement)
Google Whisk generates start and end frames. Google Flow interpolates the motion between them. ezgif.com splits the video into a 30fps image sequence. Then one prompt in Claude Code or Cursor wires the frames to play on scroll.
- **For us:** this is a premium add-on for client sites, e.g. a hero section that scrubs through a brand portrait or product reveal. It could plug into the `motion/` pipeline we already use for the TCMG explainers.

### D. Marketing skill packs (29-skill pack: 46K views; 35-skill plugin: 9K)
Both are free GitHub repos of Claude skills: content strategy, copywriting, CRO, SEO, paid ads, lead magnets, cold email, pricing, A/B tests and launch plans. Install: Settings → Capabilities → Skills → upload. For the plugin, ask Cowork to clone the repo and package it.
- **For us:** don't install these wholesale on top of the SMO/TCMG skills, because they'll compete for triggers. Mine them for frameworks (launch plan, lead magnet, pricing) and fold the useful parts into a The-Me-Dia skill set.

### E. Sandcastles `/analyze` for competitor research
Paste dozens of video URLs into one call and get the transcript, hook, format, structure and layout for each.
- **For us:** Sandcastles is already connected (it produced this report). Next step: build a watchlist of personal-brand and creator-economy channels. Then `top_hooks`, `top_formats` and `top_topics` can feed The-Me-Dia's content calendar every week.

### F. MCP stack they recommend, mapped to what we already have
| Theirs | Purpose | Our equivalent |
|---|---|---|
| Apify | ready-made scrapers | Firecrawl (out of credits right now) |
| Playwright | real browser for Claude | pre-installed in cloud sessions |
| Perplexity | cited live research | WebSearch / Firecrawl search |
| Higgsfield | image, video and UGC ad generation | ElevenLabs, AdSumo, Canva |
| Buffer | drafts posts into the queue | Metricool (connected) |

We already have this stack covered. Apify is the only gap worth looking at, and only if Firecrawl stays out of credits.

## 2. Their content formula (for The-Me-Dia's own Shorts)

Every top performer has the same shape:
1. **0–5s hook** that names a cost or a hire, then removes it:
   - "Forget [common practice]. [Tool] just did [high-value result] with [minimal effort]." (the $10K website)
   - "[Agencies] charge [$5,000] for [result]. I built one in [10 minutes]." (scroll animation)
   - "Someone just turned [tool] into [a whole department] with [29] [skills]." (marketing team)
   - "I just made [task] with [tool] in under [5 minutes]." (Canva)
2. **6–35s:** "Here's how it works." Then numbered steps ("First… Second…"), each one a single copy-paste action.
3. **~3s proof** shot of the finished result.
4. **CTA:** "Check my pinned comment for the link." The pinned comment holds the lead magnet (a setup guide that funnels to their Skool community).
- **Layout:** greenscreen of the creator over the screen recording, with on-screen text repeating the number or dollar figure for silent viewers.
- **Length:** 35–45s.

**What separates hits from misses:**
- **Hits:** a dollar anchor plus a visual result plus a creative or design outcome (website, carousel, animation).
- **Misses:** generic "N tools/settings/repos" listicles and cheap-model news. These mostly land at 0.3–0.7x.
- **Trend:** the September uploads are sliding (0.1–1.1x), which suggests the format is wearing out.
- **For The-Me-Dia:** borrow the hook and step structure, but anchor it on identity and influence outcomes rather than tool lists. For example: "Brand strategists charge $3K for this. Claude built my brand kit in 10 minutes."

## 3. Suggested next steps
1. Run the Canva carousel workflow on one real The-Me-Dia post.
2. Build a `the-me-dia-design` Claude skill (tokens, type, spacing, references), modelled on the Apple and Awesome Design skills.
3. Add a scroll-scrub hero to the next client site using the Whisk → Flow → frames pipeline.
4. Set up a Sandcastles watchlist for the niche and pull weekly hooks and topics.

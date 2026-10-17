# Client discovery questionnaires

Each client gets one folder (`<client>-discovery/`) holding its outline (`questionnaire.md`) and the built page (`index.html`), deployed to a Netlify site of the same name. The link to that site is what gets sent to the client.

| Client | Folder | Live link |
|---|---|---|
| Goodvibe Mobile Entertainment (Ryan Labelle) | `dj-discovery/` | https://goodvibe-discovery.netlify.app |
| Dharma (Akash and Katy) | not in repo yet | https://dharma-discovery.netlify.app |
| Coach Mike Dominique | not in repo yet | https://coach-mike-discovery.netlify.app |

## Standard sections every questionnaire must include

1. **About the business** (name, contact details, preferred contact method).
2. **What the client needs help with most.** A pick-all-that-apply list headed "What do you need the most help with right now?", tailored to the client's industry, followed by a required "If we could fix only one thing first, what would it be?". The build script refuses an outline without it.
3. **Goals**, including a ranking question.
4. **Biggest challenges / sales process.**
5. **Online presence, brand, website needs.**
6. **Access and logistics** (accounts, uploads, approvals, kickoff call, case-study permission).

## Outline format

Write questions as numbered lists under `## Section N: Title` headings, with the answer type in brackets:
`[Short text]`, `[Long text]`, `[Choice: A / B]`, `[Checkboxes: A / B / Other]`, `[Ranking: A / B]`, `[File upload + link]`, and combinations joined with `+` (for example `[Choice: Yes / No + details]`).

## Build and deploy

```
python3 tools/questionnaire/build.py <client>-discovery/questionnaire.md tools/questionnaire/template.html <client>-discovery/index.html "Business Name" "First name"
```

Then deploy `<client>-discovery/` to its Netlify site (Forms enabled). The cloud environment needs `netlify-mcp.netlify.app` in its allowed domains.

Branding: The-Me-Dia wordmark, "Identity to Influence" tagline and colours (ink `#1a211d`, gold `#c6a679`, cream `#fbf9f2`) are set in `build.py`. Set `AVATAR` to an image path to add the avatar to the banner.

"""Build a branded client discovery questionnaire page from an MD outline.

Usage: python3 tools/questionnaire/build.py <outline.md> tools/questionnaire/template.html <client-folder>/index.html "<Business name>" "<First name(s)>"
Required questions and the intro text are set in the constants below.
"""
import html, re, sys

md_path, tpl_path, out_path, CLIENT, FIRST = sys.argv[1:6]
md = open(md_path, encoding="utf-8").read()
tpl = open(tpl_path, encoding="utf-8").read()

GREETING = f"Hi {FIRST}"
THANKS = f"Thank you, {FIRST}. We'll review everything before our kickoff call."
INTRO = (f"{GREETING}, thanks for working with us. This is about the details only you know: the events you're proudest of, "
         "the venues and vendors you work with, where your bookings come from, and what eats up your time. "
         "Rough answers are fine, and \"not sure\" is a useful answer too. Fill it in right here, attach any event photos, "
         "logos or testimonials as you go, and press Send at the bottom.")
REQUIRED = {(1, 1), (1, 2), (5, 2), (5, 3)}
SUBLABELS = {(1, 2): ("Email and phone", "Preferred way to reach you"),
             (9, 3): ("Who makes the final call", "How fast you can review")}

e = lambda s: html.escape(s, quote=True)

def slug(s, n=None):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].rstrip("-") if n else s

def unmd(s):
    return s.replace("\\[", "[").replace("\\]", "]")

def radios(name, opts, aria, req):
    out = [f'<div class="opts row" role="radiogroup" aria-labelledby="{aria}">']
    for i, o in enumerate(opts):
        oid = f"{name}--{slug(o, 24)}"
        r = ' required=""' if req and i == 0 else ""
        out.append(f'<label class="opt" for="{oid}"><input type="radio" id="{oid}" name="{name}" value="{e(o)}"{r}><span>{e(o)}</span></label>')
    out.append("</div>")
    return "".join(out)

def checks(name, opts, aria):
    out = [f'<div class="opts grid" role="group" aria-labelledby="{aria}">']
    for o in opts:
        oid = f"{name}--{slug(o, 24)}"
        out.append(f'<label class="opt" for="{oid}"><input type="checkbox" class="many" id="{oid}" data-target="{name}" value="{e(o)}"><span>{e(o)}</span></label>')
    out.append(f'</div><input type="hidden" name="{name}" data-many="1">')
    if "Other" in opts:
        out.append(f'<div class="other"><label for="{name}-other">Other:</label><input type="text" id="{name}-other" name="{name}-other"></div>')
    return "".join(out)

def ranks(name, opts, aria):
    nums = "".join(f"<option>{i}</option>" for i in range(1, len(opts) + 1))
    out = [f'<div class="ranks" role="group" aria-labelledby="{aria}">']
    for o in opts:
        oid = f"{name}--{slug(o, 24)}"
        out.append(f'<label class="rank" for="{oid}"><select id="{oid}" data-target="{name}" data-opt="{e(o)}"><option value=""></option>{nums}</select><span>{e(o)}</span></label>')
    out.append(f'</div><input type="hidden" name="{name}" data-rank="1"><p class="warn" data-rank-warn="{name}" hidden>Each number can only be used once.</p>')
    return "".join(out)

def upload(key, aria, prompt=None):
    out = [f'<p class="sub">{e(prompt)}</p>'] if prompt else []
    out.append(f'<div class="upload" data-key="{key}"><label class="pick"><input type="file" multiple="" accept="image/*,application/pdf" aria-labelledby="{aria}"><span>Add files</span></label>'
               '<span class="note">Photos or PDFs, up to 4 here. Videos: paste a link below</span><ul class="files"></ul>')
    out += [f'<input type="file" name="{key}-file-{i}" tabindex="-1">' for i in range(1, 5)]
    out.append(f'<input type="text" name="{key}-link" aria-label="Link to more files" placeholder="Or paste a Drive or Dropbox link"></div>')
    return "".join(out)

def field(s, q, text, spec):
    name = f"q{s}-{q:02d}-{slug(text, 40)}"
    aria = f"l-{s}-{q}"
    req = (s, q) in REQUIRED
    hint = ' <span class="hint">(1 = most important)</span>' if spec.startswith("Ranking") else ""
    reqtag = ' <span class="req">Required</span>' if req else ""
    body = []
    parts = [p.strip() for p in spec.split(" + ")]
    head = parts[0]
    for part in parts:
        if part.startswith("Short text") or part.startswith("Long text"):
            tag = ("textarea", part.startswith("Long"))
            if (s, q) in SUBLABELS:
                lab = SUBLABELS[(s, q)][0]
                fid = f"{name}-{slug(lab, 24)}"
                body.append(f'<label class="sub" for="{fid}">{e(lab)}</label><input type="text" id="{fid}" name="{fid}" aria-labelledby="{aria}"{" required=\"\"" if req else ""}>')
            elif tag[1]:
                body.append(f'<textarea id="{name}" name="{name}" rows="4" aria-labelledby="{aria}"{" required=\"\"" if req else ""}></textarea>')
            else:
                body.append(f'<input type="text" id="{name}" name="{name}" aria-labelledby="{aria}"{" required=\"\"" if req else ""}>')
        elif part.startswith("choice:") or part.startswith("Choice:"):
            opts = [o.strip() for o in part.split(":", 1)[1].split(" / ")]
            rname = name
            if (s, q) in SUBLABELS:
                lab = SUBLABELS[(s, q)][1]
                rname = f"{name}-{slug(lab, 24)}"
                body.append(f'<p class="sub">{e(lab)}</p>')
            body.append(radios(rname, opts, aria, req))
        elif part.startswith("Checkboxes:"):
            body.append(checks(name, [o.strip() for o in part.split(":", 1)[1].split(" / ")], aria))
        elif part.startswith("Ranking:"):
            body.append(ranks(name, [o.strip() for o in part.split(":", 1)[1].split(" / ")], aria))
        elif part.lower().startswith("file upload"):
            body.append(upload(f"{name}-files", aria, "Sending files with this form?" if head != part else None))
        elif part == "link":
            pass  # the upload block already carries a link field
        elif part == "details":
            fid = f"{name}-details"
            body.append(f'<label class="sub" for="{fid}">Details</label><input type="text" id="{fid}" name="{fid}" aria-labelledby="{aria}">')
        else:
            raise SystemExit(f"Unknown answer type in {s}.{q}: {part}")
    return (f'<fieldset class="q"><legend id="{aria}"><span class="n">{q}.</span> {e(text)}{hint}{reqtag}</legend>'
            + "".join(body) + "</fieldset>")

if not re.search(r"need the most help", md, re.I):
    raise SystemExit("Missing the standard 'What do you need the most help with right now?' question (see tools/questionnaire/README.md).")
sections, total = [], 0
for m in re.finditer(r"^## Section (\d+): (.+?)\n(.*?)(?=^## |\Z)", md, re.S | re.M):
    s, title, block = int(m.group(1)), m.group(2).strip(), m.group(3)
    qs = []
    for qm in re.finditer(r"^(\d+)\. (.+)$", block, re.M):
        line = unmd(qm.group(2)).strip()
        tm = re.match(r"(.*)\[(.+)\]\s*$", line)
        if not tm:
            raise SystemExit(f"No answer type: {line}")
        qs.append(field(s, int(qm.group(1)), tm.group(1).strip(), tm.group(2).strip()))
    total += len(qs)
    sections.append(f'<section class="sec"><h2>{s}. {e(title)}</h2>\n' + "\n".join(qs) + "\n</section>")

BRAND_CSS = r"""
/* The-Me-Dia brand */
@font-face { font-family: "Mansfield"; src: url("https://the-me-dia.com/fonts/mansfield-bold.woff2") format("woff2"); font-weight: 700; font-display: swap; }
:root { --green: #1a211d; --gold: #c6a679; --ink: #1a211d; --grey: #5a5e56; --fill: #f6f2e9; --line: #d9d0bf; --bg: #fbf9f2; --warn: #a4452c; }
header { background: var(--ink); color: #fbf9f2; padding: 28px 16px 34px; border-bottom: 3px solid var(--gold); }
header .brandrow { display: flex; align-items: center; gap: 14px; margin-bottom: 26px; }
header .avatar { width: 52px; height: 52px; border-radius: 50%; object-fit: cover; border: 2px solid var(--gold); flex: 0 0 auto; }
header .mark { font-family: "Mansfield", "Helvetica Neue", Arial, sans-serif; font-weight: 700; font-size: 24px; letter-spacing: -0.01em; line-height: 1; color: #fbf9f2; }
header .mark b { color: var(--gold); }
header .tag { display: block; margin-top: 6px; font-size: 11px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--gold); }
header h1 { font-family: "Mansfield", "Helvetica Neue", Arial, sans-serif; color: #fbf9f2; }
header p.for { margin: 8px 0 0; color: #e8e1d5; font-size: 15px; }
.track i, .pick span, .send button { background: var(--ink); }
.track i { background: var(--gold); }
.sec h2 { border-bottom-color: var(--gold); }
legend .n { color: #8a6d3f; }
.req { color: #8a6d3f; border-color: #8a6d3f; }
.intro { border-left-color: var(--gold) !important; }
.opt:has(input:checked) { border-color: var(--gold); background: var(--fill); }
.opt input, .scale input { accent-color: var(--ink); }
.done h2 { color: var(--ink); }
footer { background: var(--ink); color: #e8e1d5; border-top: 3px solid var(--gold); }
footer .in { display: flex; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
footer .gold { color: var(--gold); }
"""
AVATAR = None  # path to an image file; embedded as a data URI when set
css = tpl[tpl.index("<style"):tpl.index("</style>") + 8]
css = re.sub(r"\.intro \{[^}]*\}", ".intro { background: var(--fill); border-left: 4px solid var(--green); padding: 14px 16px; margin: 0px 0px 8px; }", css)
css = css.replace("</style>", BRAND_CSS + "\n.upload > input[type=\"file\"] { display: none; }\n[hidden] { display: none !important; }\n</style>")
script = tpl[tpl.index("<script>"):tpl.index("</script>") + 9]
footer = re.search(r"<footer>.*?</footer>", tpl, re.S).group(0)
agency = re.search(r"<header>.*?<p>[^|]*\|\s*([^<]+)</p>", tpl, re.S).group(1).strip()

avatar_html = ""
if AVATAR:
    import base64, mimetypes
    mt = mimetypes.guess_type(AVATAR)[0] or "image/png"
    avatar_html = f'<img class="avatar" alt="" src="data:{mt};base64,{base64.b64encode(open(AVATAR, "rb").read()).decode()}">'
page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Client Discovery Questionnaire | {e(CLIENT)}</title>
{css}
</head>
<body>
<header><div class="in"><div class="brandrow">{avatar_html}<div><span class="mark">The-Me-Dia<b>.</b></span><span class="tag">Identity to Influence</span></div></div><h1>Client Discovery Questionnaire</h1><p class="for">Prepared for {e(CLIENT)}</p></div></header>
<div class="bar"><div class="in"><div class="track"><i id="prog"></i></div><span id="progtxt">0 of {total} answered</span></div></div>
<main>
<form name="client-discovery" id="f" method="POST" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="bot-field" novalidate>
<input type="hidden" name="form-name" value="client-discovery">
<p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
<div class="intro"><p>{e(INTRO)}</p></div>
<p class="saved">Your answers save on this device as you go, so you can come back and finish later. Attached files aren't saved, so add them in the same visit you press Send.</p>
{chr(10).join(sections)}
<div class="send">
<p><strong>{e(THANKS)}</strong></p>
<button type="submit" id="go">Send my answers</button>
<p id="status" role="status"></p>
</div>
</form>
<div class="done" id="done"><h2>Got it, thank you!</h2><p>{e(THANKS)}</p></div>
</main>
<footer><div class="in"><span>&copy; 2026 The-Me-Dia &middot; Ottawa / Gatineau</span><span class="gold">Identity to Influence</span></div></footer>
{script}
</body></html>
"""
page = page.replace("var STORE='draft-client-discovery'", "var STORE='draft-dj-discovery'")
open(out_path, "w", encoding="utf-8").write(page)
print(f"{len(sections)} sections, {total} questions -> {out_path}")

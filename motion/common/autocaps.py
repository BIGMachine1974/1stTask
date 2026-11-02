#!/usr/bin/env python3
"""Time a video's captions from its voiceover, instead of typing CAPS timings by hand.

usage:
  python3 motion/common/autocaps.py motion/tcmg-cost-v2            # print new window.CAPS, compare with current
  python3 motion/common/autocaps.py motion/tcmg-cost-v2 --write    # also rewrite window.CAPS in index.html

The caption TEXT stays yours: it is read from the existing window.CAPS in index.html (keeping *brass* emphasis,
| line breaks and any extra fields such as the end-card flags). Only the start/end times are replaced, using
word-level timestamps from faster-whisper on vo.mp3. The words are also saved to words.json for later
word-by-word highlighting.

Timing rules, matched to the hand-timed TCMG videos:
  start = first spoken word of the line - LEAD
  end   = next caption's start - GAP   (the last caption keeps its own end and extra fields)
"""
import argparse, difflib, json, re, sys
from pathlib import Path

LEAD, GAP, MODEL = 0.05, 0.15, "small.en"
CAP_RE = re.compile(r"""\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*(['"])(.*?)(?<!\\)\3([^\]]*)\]""")


def norm(s):
    """'$623,500.' -> '623500', "Board's" -> 'boards', '*actually' -> 'actually'."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def read_caps(html):
    m = re.search(r"window\.CAPS\s*=\s*\[(.*?)\];", html, re.S)
    if not m:
        sys.exit("no window.CAPS found in index.html")
    caps = [dict(start=float(a), end=float(b), quote=q, text=t, extra=x) for a, b, q, t, x in CAP_RE.findall(m.group(1))]
    return caps, m


def transcribe(audio, model):
    import subprocess, numpy as np
    from faster_whisper import WhisperModel
    # decode with ffmpeg (already in the pipeline) rather than faster-whisper's PyAV, which breaks on some versions
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(audio), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         check=True, capture_output=True).stdout
    samples = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    wm = WhisperModel(model, device="cpu", compute_type="int8")
    segs, _ = wm.transcribe(samples, word_timestamps=True, language="en")
    return [dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for seg in segs for w in seg.words]


def align(caps, words):
    """Map every caption line onto the spoken words and return (start, end-of-speech) per line."""
    script = [(i, norm(tok)) for i, c in enumerate(caps) for tok in re.split(r"[\s|]+", c["text"]) if norm(tok)]
    spoken = [norm(w["w"]) for w in words]
    sm = difflib.SequenceMatcher(None, [t for _, t in script], spoken, autojunk=False)
    hit = {}  # caption index -> list of matched word indices
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            hit.setdefault(script[blk.a + k][0], []).append(blk.b + k)
    times = []
    for i in range(len(caps)):
        if i in hit:
            times.append((words[min(hit[i])]["s"], words[max(hit[i])]["e"]))
        else:
            times.append(None)  # no word matched (e.g. a line that is shown but not spoken)
    return times


def build(caps, times):
    out = []
    for i, c in enumerate(caps):
        t = times[i]
        start = max(0.05, round(t[0] - LEAD, 2)) if t else c["start"]
        out.append(dict(c, start=start))
    for i, c in enumerate(out[:-1]):
        c["end"] = round(out[i + 1]["start"] - GAP, 2)
    return out


def js(caps):
    fmt = lambda v: f"{v:g}"
    return "window.CAPS=[" + ",\n".join(
        f"[{fmt(c['start'])},{fmt(c['end'])},{c['quote']}{c['text']}{c['quote']}{c['extra']}]" for c in caps) + "];"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_dir")
    ap.add_argument("--write", action="store_true", help="rewrite window.CAPS in index.html")
    ap.add_argument("--model", default=MODEL)
    a = ap.parse_args()
    d = Path(a.video_dir)
    html = (d / "index.html").read_text()
    caps, m = read_caps(html)
    words = transcribe(d / "vo.mp3", a.model)
    (d / "words.json").write_text(json.dumps(words, indent=1))
    times = align(caps, words)
    new = build(caps, times)

    print(f"{'line':<44} {'hand start':>10} {'auto start':>10} {'diff':>6}")
    for old, n, t in zip(caps, new, times):
        flag = "" if t else "  (not matched, kept hand time)"
        label = old["text"].replace("*", "").replace("|", " ")[:42]
        print(f"{label:<44} {old['start']:>10.2f} {n['start']:>10.2f} {n['start'] - old['start']:>+6.2f}{flag}")
    print("\n" + js(new))
    if a.write:
        (d / "index.html").write_text(html[:m.start()] + js(new) + html[m.end():])
        print(f"\nwrote {d / 'index.html'}")


if __name__ == "__main__":
    main()

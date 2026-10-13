"""Build word-level karaoke captions from edge-tts's sentence-level SRT.
Sentence [start,end] are exact; words are distributed across each span weighted
by length. Deterministic, stdlib-only, perfectly bounded to the voiceover."""
import re, json, os

# Resolve against the PROJECT you run this from, not the script's own folder.
# Vendored into the skill it was reading ~/.claude/.../scripts/assets/vo.srt,
# which exists for no project. Same failure mode as a hardcoded domain in a
# checker: it only breaks once the script is reused, which is the whole point
# of vendoring it.
HERE = os.environ.get("VIDEO_PROJECT", os.getcwd())
srt = open(os.path.join(HERE, "assets", "vo.srt")).read()


def to_ms(ts):
    h, m, rest = ts.split(":")
    s, ms = rest.split(",")
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(ms)


cues = []
for block in srt.strip().split("\n\n"):
    lines = block.strip().split("\n")
    if len(lines) >= 3:
        m = re.search(r"(\d\d:\d\d:\d\d,\d+)\s*-->\s*(\d\d:\d\d:\d\d,\d+)", lines[1])
        if m:
            cues.append((to_ms(m.group(1)), to_ms(m.group(2)), " ".join(lines[2:]).strip()))

caps = []
first = True
for start, end, text in cues:
    words = text.split()
    weights = [max(1.0, len(w)) for w in words]
    total = sum(weights)
    span = end - start
    t = float(start)
    for w, wt in zip(words, weights):
        d = span * wt / total
        caps.append({
            "text": ("" if first else " ") + w,
            "startMs": round(t),
            "endMs": round(t + d),
            "timestampMs": round(t + d / 2),
            "confidence": 1,
        })
        first = False
        t += d

os.makedirs(os.path.join(HERE, "src"), exist_ok=True)
json.dump(caps, open(os.path.join(HERE, "src", "captions.json"), "w"), indent=2)
print("tokens:", len(caps), "| span ms:", caps[0]["startMs"], "->", caps[-1]["endMs"])
print("preview:", json.dumps([c["text"] for c in caps[:10]]))

#!/usr/bin/env python3
"""Assemble the 24 hour files into docs/index.html and run the QA report."""
import json, re, sys, collections, pathlib

ROOT = pathlib.Path(__file__).parent
HOURS = ROOT / "hours"
SITE = ROOT / "docs"

BANNED = [
    "liminal", "luminous", "ephemeral", "gossamer", "tapestry", "symphony",
    "whisper", "soul", "sacred", "shimmer", "iridescent", "the weight of",
    "something like", "a kind of", "unspoken", "untold", "quiet hum",
    "gentle hum", "alchemy", "in this moment", "the space between",
]
EMDASH = "—"

def main():
    poems = [None] * 1440
    problems = []
    for h in range(24):
        f = HOURS / f"hour_{h:02d}.json"
        if not f.exists():
            problems.append(f"MISSING FILE: {f.name}")
            continue
        data = json.loads(f.read_text())
        arr = data["poems"]
        if len(arr) != 60:
            problems.append(f"{f.name}: {len(arr)} poems (need 60)")
            continue
        for m, p in enumerate(arr):
            poems[h * 60 + m] = p.strip()

    if any(p is None for p in poems):
        print("INCOMPLETE:")
        for pr in problems: print(" ", pr)
        sys.exit(1)

    # QA report
    print("=== QA REPORT ===")
    words = sum(len(p.split()) for p in poems)
    print(f"poems: {len(poems)}  total words: {words}")

    over = [(i, len(p.split())) for i, p in enumerate(poems) if len(p.split()) > 40]
    if over:
        print(f"OVER 40 WORDS ({len(over)}):")
        for i, n in over: print(f"  {i//60:02d}:{i%60:02d} ({n}w)")

    low = [p.lower() for p in poems]
    for b in BANNED:
        hits = [i for i, p in enumerate(low) if b in p]
        # avoid false positives: 'soul' in 'soulless'? still flag; review manually
        if hits:
            print(f"BANNED '{b}' ({len(hits)}): " + ", ".join(f"{i//60:02d}:{i%60:02d}" for i in hits[:12]))

    em = [i for i, p in enumerate(poems) if EMDASH in p]
    if em:
        print(f"EM-DASH ({len(em)}): " + ", ".join(f"{i//60:02d}:{i%60:02d}" for i in em[:20]))

    exact = collections.Counter(low)
    dupes = [k for k, v in exact.items() if v > 1]
    if dupes:
        print(f"EXACT DUPES ({len(dupes)}):")
        for k in dupes[:10]: print("  " + k[:60].replace("\n", " / "))

    # near-dupes: first 4 words
    starts = collections.Counter(" ".join(re.findall(r"[a-z']+", p))[:999] and " ".join(re.findall(r"[a-z']+", p)[:4]) for p in low)
    ndup = {k: v for k, v in starts.items() if v > 2 and k}
    if ndup:
        print(f"REPEATED OPENINGS (>2): {len(ndup)}")
        for k, v in sorted(ndup.items(), key=lambda x: -x[1])[:15]:
            print(f"  {v}x  '{k}'")

    # overused vocabulary across whole book
    vocab = collections.Counter(w for p in low for w in re.findall(r"[a-z']+", p))
    watch = ["light", "dark", "silence", "silent", "moon", "coffee", "kitchen",
             "quiet", "still", "small", "somewhere", "night", "morning"]
    print("WATCH-WORD COUNTS: " + "  ".join(f"{w}:{vocab[w]}" for w in watch))

    if "--report-only" in sys.argv:
        return

    # Build site
    SITE.mkdir(exist_ok=True)
    tpl = (ROOT / "template.html").read_text()
    out = tpl.replace("__POEMS__", json.dumps(poems, ensure_ascii=False))
    out = out.replace("__WORDCOUNT__", f"{words:,}")
    (SITE / "index.html").write_text(out)
    print(f"\nwrote docs/index.html ({len(out)//1024} KB)")

if __name__ == "__main__":
    main()

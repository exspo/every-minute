#!/usr/bin/env python3
"""Image-level duplicate gate (Destroyer r3 prescription). Every poem carries
1-3 image tags (hours_tags/). Invariant: no SPECIFIC image tag appears in two
different hours inside a 180-minute circular window without an adjudication
entry. Generic day-texture families (bar, meeting, dishwasher, ...) are
adjudicated as families in ADJUDICATION.md and screened by the lexical gate
(gate_v2.py) instead; same-hour repeats are one author's deliberate sequencing."""
import json, re, pathlib, collections, itertools

ROOT = pathlib.Path(__file__).parent
poems, tags = [None] * 1440, [None] * 1440
for h in range(24):
    d = json.loads((ROOT / "hours" / f"hour_{h:02d}.json").read_text())
    t = json.loads((ROOT / "hours_tags" / f"hour_{h:02d}.json").read_text())
    assert len(t["tags"]) == 60, f"hour {h}"
    for m in range(60):
        poems[h * 60 + m] = d["poems"][m]
        tags[h * 60 + m] = [x.lower().strip() for x in t["tags"][m]]

def stem(w):
    for suf in ("ing", "es", "ed", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: len(w) - len(suf)]
    return w

def norm(tag):
    return "-".join(stem(w) for w in re.split(r"[-_ ]+", tag) if w)

ntags = [set(norm(t) for t in tl) for tl in tags]

# Generic families: the day's shared furniture. Density inside these is the
# hour's assigned subject; the family-level curation is recorded in
# ADJUDICATION.md and same-joke pairs inside them are hunted lexically.
GENERIC = {"dog","cat","phone","coffee","car","kitchen","meeting","meet","school","bus","office",
 "list-form","definition-form","instruction-form","overheard","receipt-form","insomnia","insomnia-math",
 "email","alarm","alarm-clock","dinner","tv","sink","door","window","traffic","commute","breakfast",
 "homework","teenager","nurse","baker","clock","bar","lunch","park-lot","park-car","minute-itself",
 "night-shift","new-father","grandmother","cross-guard","time-zone","to-do-list","couple","couch",
 "porch","radio","truck","warehouse","shower","moth","porch-light","bakery","bread","dough","onion",
 "pan","pans","kettle","dishwasher","practice-pickup","school-bus","bath","bedtime","bike","argument",
 "pen","pigeon","backpack","elevator","procrastination","sleep-math","chair","child","classroom","oven",
 "recipe","pack-lunch","forklift","gym","trash","mother","streetlight","streetlamp","hospital","baby",
 "text-message","phone-call","pickup-line","dish","sandwich","soup","mug","nap","sign","sock","pipe",
 "boot","banana","bagel","book","blanket","badge","bench","bottle","airport","afternoon","workday",
 "leftover","latenes","jogger","hose","highway","garage","garage-door","gas-station","freight-train",
 "fold-chair","fork","fish-tank","empty-house","empty-room","driveway","dumpster","delivery-truck",
 "convenience-store","commuter","counter","cereal-bowl","ceil-fan","car-door","car-nap","car-radio",
 "break-room","office-fridge","office-jargon","office-chair","load-dock","look-busy","kitchen-counter",
 "grocery-list","grocery-stocker","good-chair","gett-up","wait-line","waking","water-heater","routine",
 "regret","roofer","rooster","red-eye-flight","refrigerator","scaffold","school-bell","screen-door",
 "second-coffee","second-wind","security-guard","sidewalk","sleep-kid","snooze","stairwell","stapler",
 "spreadsheet","third-shift","toaster","traffic-cone","truck-stop","unsent-text","vend-machine",
 "water-glas","night-nurse","intrusive-memory","ice-machine","ice-maker","last-call","mail-carrier",
 "mail-truck","mail-slot","microwav-fish","clock-digit","one-more-episode","dryer-buzzer","pot-of-water",
 "pharmacy","phone-battery","pretzel","printer","podcast","neighbor","nightstand","gym-bag"}

T = lambda h, m: h * 60 + m
# Adjudicated specific-tag keeps (reason per line):
KEEP_PAIRS = {tuple(sorted(p)) for p in [
    (T(6, 31), T(8, 47)),    # shift-change: arrival smell / aftermath coffee
    (T(5, 35), T(6, 26)),    # rehearsal: mirror practice / rehearsed grievance gone
    (T(1, 22), T(23, 16)),   # gutters: street hubcap / roof downspout
    (T(5, 0), T(7, 8)),      # coffee maker: timer / instruction form
    (T(15, 5), T(16, 7)),    # copier: favor / jams for the credentialed
    (T(15, 52), T(16, 44)),  # slump: soft spot / what came instead
    (T(19, 59), T(20, 0)),   # accidental sequence: plate in, machine starts
    (T(19, 3), T(20, 38)),   # practice keeps: joke / crowd
    (T(19, 3), T(21, 16)),   # practice keeps: joke / smell
    (T(20, 38), T(21, 16)),  # practice keeps: crowd / smell
    (T(0, 2), T(3, 0)),      # night machines: glowing / thinking about the dollar
]}

def cdist(i, j):
    d = abs(i - j)
    return min(d, 1440 - d)

bytag = collections.defaultdict(list)
for i, tl in enumerate(ntags):
    for t in tl:
        bytag[t].append(i)

out = []
for t, idxs in bytag.items():
    if t in GENERIC:
        continue
    for a, b in itertools.combinations(idxs, 2):
        if a // 60 == b // 60:
            continue
        if tuple(sorted((a, b))) in KEEP_PAIRS:
            continue
        if cdist(a, b) <= 180:
            out.append((t, cdist(a, b), a, b))

print(f"IMAGE COLLISIONS (specific tags, cross-hour, <=180m, minus keeps): {len(out)}")
for t, d, i, j in sorted(out):
    print(f"{t:24s} d={d:3d} [{i//60:02d}:{i%60:02d}] {poems[i][:52].replace(chr(10), ' / ')}")
    print(f"{'':24s}       [{j//60:02d}:{j%60:02d}] {poems[j][:52].replace(chr(10), ' / ')}")

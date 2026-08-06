#!/usr/bin/env python3
"""Image-level duplicate gate, v3 (Destroyer r4 redesign).

Changes from v2, each answering an r4 finding:
- Tags are canonicalized through SYNONYMS before any check, so granularity
  variants (trash-bag / trash-night / recycling-bin / dumpster) collide.
- KEEP_PAIRS is consulted INSIDE the pair loop, before any family exemption —
  no unreachable annotations.
- The exemption list is gone. TEXTURE (true furniture words) is exempt from
  the pair check only, and the gate REPORTS how many pairs it suppressed.
- A density report covers every canonical tag including texture: max
  instances in any 90-minute circular window; >3 is a flag.
"""
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

# Canonical vocabulary: map granularity variants onto one scene label.
SYNONYMS = {}
def syn(canon, *variants):
    for v in variants:
        SYNONYMS[norm(v)] = canon
syn("trash", "trash", "trash-bag", "trash-can", "trash-night", "trash-curb",
    "recycling-bin", "recycling", "dumpster", "garbage", "bin-curb")
syn("sports-practice", "practice", "practice-pickup", "gym-bag", "rink",
    "duffel-bag", "cleats", "sports", "little-league")
syn("bar", "bar", "bar-door", "bartender", "bar-tab", "last-call", "bar-close",
    "bar-kitchen-close", "tab")
syn("dryer", "dryer", "dryer-buzzer", "laundry", "hamper", "laundromat")
syn("ice-machine", "ice-machine", "ice-maker")
syn("vending", "vend-machine", "vending-machine", "vending", "candy-machine")
syn("alarm", "alarm", "alarm-clock", "snooze", "alarms")
syn("microwave", "microwave", "microwav-fish", "microwave-fish")
syn("moth", "moth", "moths")
syn("printer", "printer", "copier")
syn("phone-glow", "phone-glow", "blue-glow", "screen-glow")
syn("coffee-machine", "coffee-maker", "coffee-pot", "percolator")
syn("city-bus", "bus", "city-bus", "bus-stop", "bus-shelter")
syn("school-bus", "school-bus")
syn("meeting", "meet", "meeting", "conference-call", "standup")
syn("nurse", "nurse", "night-nurse", "nurse-charting")
syn("baker", "baker", "bakery", "dough", "bread", "proofing")
syn("crossing-guard", "cross-guard", "crossing-guard")
syn("grandmother", "grandmother", "grandma")
syn("new-father", "new-father", "new-parent")
syn("kettle", "kettle", "teakettle")
syn("dishwasher", "dishwasher")
syn("porch-light", "porch-light", "porch-bulb")
syn("unsent-text", "unsent-text", "deleted-text", "drafted-text")
syn("dog", "dog", "old-dog", "dog-walk", "dog-tags", "leash", "dogs")
syn("cat", "cat", "cats", "house-cat")
syn("left-on-light", "porch-light", "porch-bulb", "kitchen-light", "stove-light", "oven-light")
syn("plan", "day-plan", "morning-plan", "abandoned-plan", "before-work-plan",
    "to-do-list", "mental-list", "plan-decay")
syn("sleep-math", "sleep-math", "insomnia-math")
syn("shopping-cart", "shopping-cart", "cart-corral", "stray-cart")

def canon(tag):
    n = norm(tag)
    return SYNONYMS.get(n, n)

ctags = [set(canon(t) for t in tl) for tl in tags]

# True furniture: words so ubiquitous in domestic life that pairwise identity
# says nothing. Exempt from the PAIR check only; still in the density report.
TEXTURE = {"kitchen", "door", "window", "chair", "table", "car", "phone", "house",
           "street", "hallway", "counter", "wall", "floor", "morning", "evening",
           "office", "school", "coffee", "lunch", "dinner", "breakfast", "sleep",
           "bed", "tv", "couch", "clock", "light", "sink", "traffic", "commute",
           "work", "workday", "afternoon", "child", "kid", "parent", "family"}

# Suites: documented choruses (ADJUDICATION.md lists members and the
# distinctness basis). Pair-check off; membership and density PRINTED.
SUITES = {"baker", "nurse", "alarm", "bar", "email", "inbox", "meeting",
          "homework", "plan", "sleep-math", "couple", "city-bus",
          "trash", "overheard", "minute-itself", "dog", "cat", "left-on-light",
          "argument", "regret", "procrastination", "hunger", "wait", "routine",
          "neighbor", "latenes", "text-message", "phone-call", "radio", "truck",
          "warehouse", "teenager", "mother", "grandmother", "new-father",
          "night-shift", "time-zone", "insomnia", "bedtime", "park-lot", "park-car",
          "list-form", "definition-form", "instruction-form", "receipt-form"}

T = lambda h, m: h * 60 + m
KEEP_PAIRS = {
    tuple(sorted(p)): why for p, why in [
        ((T(0, 15), T(2, 34)), "hospital: ice-chips / er-doors"),
        ((T(0, 15), T(2, 7)), "hospital: ice-chips / nurse"),
        ((T(0, 17), T(3, 15)), "refrigerator: 12:17 a.m. the refrigerator / quarter past. the refrigerator"),
        ((T(0, 19), T(1, 29)), "new-father: hallway-pacing / bottle"),
        ((T(0, 19), T(2, 18)), "new-father: hallway-pacing / documentary"),
        ((T(0, 19), T(22, 17)), "new-father: hallway-pacing / baby"),
        ((T(0, 19), T(3, 16)), "new-father: hallway-pacing / swaying"),
        ((T(0, 2), T(3, 0)), "vending: a vending machine glowing / the vending machine on"),
        ((T(0, 26), T(2, 52)), "highway: truck / cruise-control"),
        ((T(0, 3), T(22, 17)), "baby: the baby is asleep / new-parent"),
        ((T(0, 31), T(2, 12)), "convenience-store: roller-grill / receipt-form"),
        ((T(0, 32), T(21, 47)), "porch: screen-door / citronella-candle"),
        ((T(0, 4), T(2, 33)), "unsent-text: open-all-night+list-form / drafted, deleted, drafted again"),
        ((T(1, 12), T(2, 48)), "ceil-fan: argument / 2:48. the ceiling fan"),
        ((T(1, 12), T(23, 33)), "ceil-fan: argument / ceiling fan on low"),
        ((T(1, 17), T(22, 40)), "second-wind: definition-form / at 10:40 the second"),
        ((T(1, 22), T(23, 16)), "gutter: hubcap / rain or no rain"),
        ((T(1, 29), T(2, 18)), "new-father: bottle / documentary"),
        ((T(1, 29), T(3, 16)), "new-father: bottle / swaying"),
        ((T(1, 41), T(4, 25)), "airport: highway-sign / ramp-crew"),
        ((T(1, 43), T(3, 55)), "security-guard: paperback / the security guard walks"),
        ((T(1, 48), T(23, 44)), "grocery-list: list-form / 11:44 p.m. the grocery"),
        ((T(10, 10), T(12, 12)), "clock-digit: minute-itself / 12:12. the one minute"),
        ((T(10, 10), T(12, 34)), "clock-digit: minute-itself / 12:34. four numbers in"),
        ((T(10, 29), T(13, 22)), "forklift: the forklift beeps in / warehouse"),
        ((T(10, 35), T(12, 0)), "sandwich: crane-operator / office-building"),
        ((T(10, 35), T(12, 44)), "sandwich: crane-operator / diagonal-cut"),
        ((T(10, 35), T(12, 51)), "sandwich: crane-operator / auto-shop"),
        ((T(10, 46), T(13, 41)), "load-dock: the truck backs into / delivery-truck"),
        ((T(11, 29), T(14, 27)), "school-bell: kids / 2:27 p.m. the bell"),
        ((T(11, 34), T(13, 47)), "office-jargon: meeting / circle-back"),
        ((T(11, 54), T(12, 46)), "soup: lunch / your soup is hotter"),
        ((T(12, 19), T(14, 43)), "bench: outdoors / dialysis-center"),
        ((T(12, 24), T(15, 19)), "sign: card-reader / traffic-cones"),
        ((T(12, 57), T(15, 43)), "pen: lunch-bag / car"),
        ((T(12, 9), T(13, 0)), "office-fridge: list-form / tupperware"),
        ((T(13, 41), T(14, 8)), "load-dock: delivery-truck / warehouse"),
        ((T(13, 41), T(16, 17)), "delivery-truck: loading-dock / a ups truck double-parked"),
        ((T(13, 43), T(15, 37)), "spreadsheet: 1:43. two people are / 3:37. the spreadsheet scrolls"),
        ((T(13, 45), T(16, 22)), "onion: prep-cook / onions bought, not yet"),
        ((T(13, 53), T(16, 41)), "dishwasher: commercial-kitchen / the dishwasher is loaded"),
        ((T(14, 27), T(15, 0)), "school-bell: 2:27 p.m. the bell / school-door"),
        ((T(14, 28), T(16, 30)), "stapler: 2:28. a stapler borrowed / tea+cigarette"),
        ((T(14, 39), T(16, 3)), "classroom: dismissal / teacher"),
        ((T(14, 40), T(15, 11)), "school-bus: definition-form / argument"),
        ((T(14, 40), T(16, 11)), "school-bus: definition-form / sleeping-kid"),
        ((T(14, 44), T(15, 34)), "fold-chair: gym / warning-label"),
        ((T(14, 44), T(15, 55)), "gym: folding-chairs / parking-lot"),
        ((T(14, 55), T(15, 26)), "backpack: classroom / school-folder"),
        ((T(14, 55), T(16, 3)), "classroom: backpacks / teacher"),
        ((T(14, 55), T(17, 13)), "backpack: classroom / child"),
        ((T(14, 58), T(17, 41)), "pickup-line: podcast / instruction-form"),
        ((T(14, 58), T(17, 49)), "pickup-line: podcast / the pickup line has"),
        ((T(15, 1), T(17, 8)), "crossing-guard: minivan / vest"),
        ((T(15, 11), T(16, 11)), "school-bus: argument / sleeping-kid"),
        ((T(15, 13), T(17, 3)), "grocery-list: the errand list with the-thing-for-the-sink / tonight's dinner mise"),
        ((T(15, 22), T(16, 50)), "look-busy: self-instruction to be busy / the good ones performing busyness at ten to five"),
        ((T(15, 24), T(16, 36)), "pretzel: apple / an open bag of"),
        ((T(15, 26), T(17, 13)), "backpack: school-folder / child"),
        ((T(15, 34), T(17, 46)), "fold-chair: warning-label / lawn"),
        ((T(15, 39), T(18, 14)), "refrigerator: refrigerator open. no plan / someone stands in the"),
        ((T(15, 5), T(16, 7)), "printer: the copier warms up / at 4:07 the copier"),
        ((T(15, 58), T(18, 52)), "recipe: 3:58. a recipe read / salt"),
        ((T(15, 8), T(17, 58)), "garage-door: basketball / homecoming"),
        ((T(16, 22), T(18, 0)), "onion: onions bought, not yet / house"),
        ((T(16, 22), T(18, 21)), "onion: onions bought, not yet / pan"),
        ((T(16, 41), T(17, 44)), "dishwasher: the dishwasher is loaded / the dishwasher from last"),
        ((T(16, 9), T(17, 0)), "office-chair: back-pain / parking-deck"),
        ((T(17, 12), T(19, 0)), "oven: 5:12. the oven preheats / lasagna"),
        ((T(17, 12), T(19, 43)), "oven: 5:12. the oven preheats / recipe"),
        ((T(17, 19), T(18, 21)), "pan: eggs / onions"),
        ((T(17, 20), T(18, 25)), "pans: dusk / improvised-plan"),
        ((T(17, 39), T(20, 26)), "forklift: two forklifts, nose to / a forklift beeping at"),
        ((T(17, 44), T(19, 59)), "dishwasher: the dishwasher from last / last-plate"),
        ((T(17, 44), T(20, 0)), "dishwasher: the dishwasher from last / the dishwasher starts its"),
        ((T(17, 47), T(18, 29)), "commuter: traffic / bus"),
        ((T(17, 59), T(18, 21)), "pan: fish / onions"),
        ((T(18, 50), T(19, 19)), "fork: plates / argument"),
        ((T(18, 52), T(19, 43)), "recipe: salt / oven"),
        ((T(18, 58), T(19, 49)), "screen-door: neighbor-cooking / july"),
        ((T(19, 21), T(21, 37)), "leftover: mismatched-lid / nobody in this house"),
        ((T(19, 26), T(20, 30)), "dish: homework / kitchen"),
        ((T(19, 3), T(20, 38)), "sports-practice: practice ends at seven / the last practice of"),
        ((T(19, 3), T(21, 16)), "sports-practice: practice ends at seven / practice ran late. the"),
        ((T(19, 37), T(21, 36)), "mug: kettle / cold-coffee"),
        ((T(19, 38), T(20, 30)), "dish: oldest-kid / kitchen"),
        ((T(19, 40), T(20, 49)), "grandmother: dinner-hour / phone-call"),
        ((T(19, 59), T(20, 0)), "dishwasher: last-plate / the dishwasher starts its"),
        ((T(2, 15), T(3, 19)), "intrusive-memory: old-name / 3:19 a.m. the mind"),
        ((T(2, 18), T(3, 16)), "new-father: documentary / swaying"),
        ((T(2, 28), T(5, 8)), "gett-up: you could get up / bare-feet"),
        ((T(2, 3), T(4, 33)), "red-eye-flight: beverage-cart / cabin-crew"),
        ((T(2, 31), T(4, 15)), "truck-stop: truck stop, shower seven / receipt-form"),
        ((T(2, 49), T(23, 53)), "dryer: the dryer downstairs finishes / 11:53 p.m. the hamper"),
        ((T(20, 16), T(21, 47)), "porch: couple / citronella-candle"),
        ((T(20, 25), T(21, 46)), "sleep-kid: couch / shoes"),
        ((T(20, 31), T(21, 9)), "cereal-bowl: instruction-form / teenager"),
        ((T(20, 38), T(21, 16)), "sports-practice: the last practice of / practice ran late. the"),
        ((T(20, 42), T(22, 53)), "garage: procrastination / a garage door closing"),
        ((T(20, 5), T(22, 53)), "garage: game-on-tv / a garage door closing"),
        ((T(21, 11), T(23, 23)), "nightstand: phone-buzz / phone"),
        ((T(21, 23), T(22, 26)), "gas-station: text-message / hot-dog"),
        ((T(21, 24), T(23, 21)), "dryer: the dryer buzzes. everybody / the laundry got folded"),
        ((T(21, 24), T(23, 53)), "dryer: the dryer buzzes. everybody / 11:53 p.m. the hamper"),
        ((T(21, 25), T(22, 36)), "blanket: couple / thermostat"),
        ((T(21, 50), T(22, 38)), "bike: lawn / a bike chained to"),
        ((T(3, 15), T(4, 27)), "refrigerator: quarter past. the refrigerator / label-form"),
        ((T(3, 28), T(4, 52)), "third-shift: definition-form / drive-home"),
        ((T(4, 3), T(7, 0)), "sock: somewhere a man puts / toaster"),
        ((T(4, 50), T(5, 16)), "shower: house / email"),
        ((T(4, 50), T(5, 50)), "shower: house / time-math"),
        ((T(4, 50), T(6, 30)), "shower: house / water-pressure"),
        ((T(5, 0), T(7, 8)), "coffee-machine: dog / instruction-form"),
        ((T(5, 16), T(6, 30)), "shower: email / water-pressure"),
        ((T(5, 20), T(8, 10)), "stairwell overheard: I-said-five-I-meant-five / she-knows-she-just-doesn't-know-know"),
        ((T(5, 25), T(8, 19)), "car-radio: hymn / parking-lot"),
        ((T(5, 27), T(6, 54)), "empty-room: reps / alarm-clock"),
        ((T(5, 35), T(6, 26)), "rehears-speech: bathroom-fan / six twenty-six. whatever you"),
        ((T(5, 50), T(6, 30)), "shower: time-math / water-pressure"),
        ((T(6, 17), T(7, 17)), "crossing-guard: a crossing guard's vest / a crossing guard adjusts"),
        ((T(6, 18), T(7, 2)), "pack-lunch: prophecy of the forgotten note / the turkey-no-crust manifest"),
        ((T(6, 31), T(8, 47)), "shift-change: 6:31. day shift arrives / coffee"),
        ((T(6, 34), T(8, 46)), "backpack: doorway / train-doors"),
        ((T(6, 44), T(7, 13)), "podcast: the third-favorite podcast, because / the podcast host is"),
        ((T(6, 46), T(7, 11)), "banana: train-platform / a banana on the"),
        ((T(6, 52), T(7, 29)), "elevator: rehearsing-name / nurse"),
        ((T(6, 52), T(8, 35)), "elevator: rehearsing-name / everyone in this elevator"),
        ((T(6, 59), T(7, 59)), "empty-house: furnace / 7:59. the house, briefly"),
        ((T(7, 17), T(9, 31)), "crossing-guard: a crossing guard adjusts / parked-car"),
        ((T(7, 18), T(9, 16)), "grandmother: somebody's grandmother has been / bank-line"),
        ((T(7, 29), T(8, 35)), "elevator: nurse / everyone in this elevator"),
        ((T(7, 48), T(8, 56)), "jogger: trash-can / a woman jogs the"),
        ((T(7, 9), T(8, 2)), "school-bus: the bus makes its / stop-arm"),
        ((T(7, 9), T(8, 43)), "school-bus: the bus makes its / a school bus, empty"),
        ((T(8, 4), T(11, 1)), "bagel: the bagel is toasting / second-bagel"),
        ((T(8, 9), T(9, 2)), "badge: your badge is in / a badge flipped backward"),
        ((T(9, 14), T(10, 20)), "mail-carrier: mail-truck / dogs"),
        ((T(9, 14), T(11, 48)), "mail-truck: mail-carrier / the mail truck stops"),
        ((T(9, 28), T(10, 42)), "roofer: two hours in, the / radio"),
        ((T(9, 34), T(11, 41)), "pharmacy: waiting-line / waiting"),
        ((T(9, 44), T(11, 47)), "new-father: new parents have been / sleep"),
        ((T(9, 48), T(10, 7)), "printer: 9:48, and the printer / at 10:07 the printer"),
    ]
}

def cdist(i, j):
    d = abs(i - j)
    return min(d, 1440 - d)

bytag = collections.defaultdict(list)
for i, tl in enumerate(ctags):
    for t in tl:
        bytag[t].append(i)

out, suppressed, keeps_hit, samehour = [], 0, set(), []
for t, idxs in bytag.items():
    for a, b in itertools.combinations(idxs, 2):
        if a // 60 == b // 60:
            if t not in TEXTURE:
                samehour.append((t, a, b))
            continue
        if cdist(a, b) > 180:
            continue
        k = tuple(sorted((a, b)))
        if k in KEEP_PAIRS:
            keeps_hit.add(k)
            continue
        if t in TEXTURE or t in SUITES:
            suppressed += 1
            continue
        out.append((t, cdist(a, b), a, b))

dead = [k for k in KEEP_PAIRS if k not in keeps_hit]
print(f"IMAGE COLLISIONS (canonical tags, cross-hour, <=180m): {len(out)}")
print(f"keeps applied: {len(keeps_hit)}; keeps never consulted (decoration, prune): {len(dead)}")
print(f"pairs suppressed as TEXTURE/SUITES after keep check (reported): {suppressed}")
tex_stat = collections.defaultdict(list)
for t2, idxs in bytag.items():
    if t2 not in TEXTURE:
        continue
    for a, b in itertools.combinations(idxs, 2):
        if a // 60 != b // 60 and cdist(a, b) <= 180:
            tex_stat[t2].append((cdist(a, b), a, b))
print("\nTEXTURE per-member suppression (count; closest pair sampled):")
for t2, ps in sorted(tex_stat.items(), key=lambda x: -len(x[1])):
    d, a, b = min(ps)
    print(f"  {t2:12s} {len(ps):3d} pairs; closest d={d}m [{a//60:02d}:{a%60:02d}] {poems[a][:34]!r} ~ [{b//60:02d}:{b%60:02d}] {poems[b][:34]!r}")

print(f"SAME-HOUR identical-tag pairs (non-texture; author-sequencing claim, verify by reading): {len(samehour)}")
for t, a, b in sorted(samehour):
    print(f"  {t:22s} [{a//60:02d}:{a%60:02d}] {poems[a][:44].replace(chr(10),' / ')}")
    print(f"  {'':22s} [{b//60:02d}:{b%60:02d}] {poems[b][:44].replace(chr(10),' / ')}")
for t, d, i, j in sorted(out):
    print(f"{t:24s} d={d:3d} [{i//60:02d}:{i%60:02d}] {poems[i][:52].replace(chr(10), ' / ')}")
    print(f"{'':24s}       [{j//60:02d}:{j%60:02d}] {poems[j][:52].replace(chr(10), ' / ')}")

# Density: every canonical tag, max instances in any 90-minute circular window
print("\nSUITE MEMBERSHIP (adjudicated choruses, printed not hidden):")
for s in sorted(SUITES):
    idxs = bytag.get(s, [])
    if idxs:
        print(f"  {s} ({len(idxs)}): " + " ".join(f"{i//60:02d}:{i%60:02d}" for i in sorted(idxs)))

FORM_EXEMPT = {"list-form", "definition-form", "instruction-form", "receipt-form",
               "overheard", "minute-itself"}  # BRIEF-mandated found-forms + the book's spine
print("\nDENSITY (max instances of a canonical tag in any 90-min window, spanning 2+ hours; flag > 3):")
flagged = []
for t, idxs in bytag.items():
    if len(idxs) < 4 or t in FORM_EXEMPT:
        continue
    best = 0
    for i in idxs:
        near = [j for j in idxs if cdist(i, j) <= 45]
        if len({j // 60 for j in near}) < 2:
            continue
        best = max(best, len(near))
    if best > 3:
        flagged.append((best, t, sorted(idxs)))
for best, t, idxs in sorted(flagged, reverse=True):
    mins = " ".join(f"{i//60:02d}:{i%60:02d}" for i in idxs)
    print(f"  {best}x {t}: {mins}")
if not flagged:
    print("  none over 3")

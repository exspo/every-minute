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

def canon(tag):
    n = norm(tag)
    return SYNONYMS.get(n, n)

ctags = [set(canon(t) for t in tl) for tl in tags]

# True furniture: words so ubiquitous in domestic life that pairwise identity
# says nothing. Exempt from the PAIR check only; still in the density report.
TEXTURE = {"kitchen", "door", "window", "chair", "table", "car", "phone", "house",
           "street", "hallway", "counter", "wall", "floor", "morning", "evening",
           "list-form", "definition-form", "instruction-form", "receipt-form",
           "overheard", "minute-itself", "insomnia", "insomnia-math", "time-zone",
           "night-shift", "office", "school", "dog", "cat", "coffee", "lunch",
           "dinner", "breakfast", "sleep", "bed", "bedtime", "tv", "couch",
           "clock", "light", "sink", "traffic", "commute", "work", "workday",
           "afternoon", "child", "kid", "teenager", "parent", "mother", "family",
           "park-lot", "park-car", "truck", "warehouse", "phone-call", "argument",
           "radio", "hunger", "wait", "lunch", "regret", "neighbor", "routine",
           "procrastination", "latenes", "text-message"}

# Suites: documented choruses (ADJUDICATION.md lists members and the
# distinctness basis). Pair-check off; membership and density PRINTED.
SUITES = {"baker", "nurse", "alarm", "bar", "email", "inbox", "meeting",
          "homework", "to-do-list", "sleep-math", "couple", "city-bus",
          "trash", "overheard", "minute-itself"}

T = lambda h, m: h * 60 + m
KEEP_PAIRS = {
    tuple(sorted(p)): why for p, why in [
        ((T(6, 31), T(8, 47)), "shift-change: arrival smell / aftermath coffee"),
        ((T(5, 35), T(6, 26)), "rehearsal: mirror practice / rehearsed grievance gone"),
        ((T(1, 22), T(23, 16)), "gutters: street hubcap / roof downspout"),
        ((T(5, 0), T(7, 8)), "coffee machine: timer personification / instruction form"),
        ((T(15, 5), T(16, 7)), "copier: favor / jams for the credentialed"),
        ((T(9, 48), T(10, 7)), "printer: needs a person / decides (adjacent-hour sequence)"),
        ((T(15, 52), T(16, 44)), "slump: soft spot / what came instead"),
        ((T(19, 59), T(20, 0)), "accidental sequence: plate in, machine starts"),
        ((T(19, 3), T(20, 38)), "practice keeps: joke / crowd"),
        ((T(19, 3), T(21, 16)), "practice keeps: joke / smell"),
        ((T(20, 38), T(21, 16)), "practice keeps: crowd / smell"),
        ((T(0, 2), T(3, 0)), "night vending: glowing / thinking about the dollar"),
        ((T(0, 55), T(1, 10)), "(retired pair)"),
        ((T(2, 43), T(3, 4)), "bakers' alarms: twenty minutes out / first second baker"),
        ((T(3, 59), T(4, 30)), "alarm suite: set across town / disciplined and doomed"),
        ((T(4, 30), T(6, 1)), "alarm suite: disciplined / couple one minute apart"),
        ((T(6, 1), T(7, 35)), "alarm suite: couple / fourth time"),
        ((T(6, 54), T(7, 35)), "alarm suite: empty room / fourth time"),
        ((T(4, 30), T(6, 54)), "alarm suite"),
        ((T(3, 4), T(4, 30)), "alarm suite"),
        ((T(2, 43), T(3, 59)), "alarm suite"),
        ((T(2, 43), T(4, 30)), "alarm suite"),
        ((T(3, 4), T(3, 59)), "(same-band alarms, distinct jokes)"),
        ((T(3, 59), T(6, 1)), "alarm suite"),
        ((T(3, 4), T(6, 1)), "alarm suite"),
        ((T(0, 27), T(2, 43)), "alarm suite: set for 4:40 / bakers'"),
        ((T(0, 27), T(3, 4)), "alarm suite"),
        ((T(13, 13), T(16, 45)), "alarms: nobody admits / shift at five"),
        ((T(16, 45), T(18, 23)), "shifts: alarm for five / badge scanned"),
        ((T(20, 33), T(21, 4)), "bar: second-drink pace / volume (distinct beats)"),
        ((T(20, 54), T(21, 4)), "bar: door leaks a song / volume"),
        ((T(20, 33), T(20, 54)), "(same-hour)"),
        ((T(20, 54), T(21, 44)), "bar: door song / outside conversation"),
        ((T(20, 33), T(21, 44)), "bar: pace / outside conversation"),
        ((T(21, 4), T(21, 44)), "(same-hour)"),
        ((T(22, 39), T(21, 4)), "bar: tab history / volume"),
        ((T(22, 39), T(21, 44)), "bar: tab / outside conversation"),
        ((T(22, 39), T(20, 54)), "bar: tab / door song"),
        ((T(22, 39), T(20, 33)), "bar: tab / pace"),
        ((T(23, 27), T(22, 39)), "bar: empties wrong order / tab"),
        ((T(23, 27), T(21, 44)), "bar: empties / outside"),
        ((T(23, 27), T(21, 4)), "bar: empties / volume"),
        ((T(1, 5), T(23, 27)), "bar: last call unmoved / empties wrong order"),
        ((T(1, 5), T(1, 50)), "(same-hour)"),
        ((T(1, 50), T(23, 27)), "bar: last song / empties"),
        ((T(19, 24), T(20, 33)), "bar: appetizer dinner / second-drink pace"),
        ((T(19, 24), T(20, 54)), "bar: appetizer / door song"),
        ((T(19, 24), T(21, 4)), "bar: appetizer / volume"),
        ((T(19, 24), T(21, 44)), "bar: appetizer / outside"),
        ((T(17, 40), T(19, 24)), "bar: bathtub fill / appetizer dinner"),
        ((T(16, 27), T(17, 40)), "bar: door propped open / bathtub fill"),
        ((T(9, 6), T(10, 6)), "nurse charting arc"),
        ((T(5, 6), T(6, 31)), "night nurse: last vitals / handoff smell"),
        ((T(22, 52), T(23, 54)), "night nurse: learns the caller / writes the time"),
        ((T(20, 15), T(18, 41)), "eats standing mirror"),
        ((T(2, 14), T(4, 11)), "baker: dough unsupervised / proof definition"),
        ((T(4, 11), T(5, 3)), "baker: proof definition / doubled overnight"),
        ((T(2, 14), T(5, 3)), "baker: walk-in / doubled"),
        ((T(3, 58), T(4, 58)), "baker: whiteboard / bread out"),
        ((T(4, 58), T(5, 3)), "(adjacent baker beats)"),
        ((T(4, 58), T(6, 36)), "baker: bread out / toast by six"),
        ((T(5, 3), T(6, 36)), "baker beats"),
        ((T(5, 7), T(6, 36)), "baker: ingredients / toast"),
        ((T(5, 17), T(6, 36)), "baker: proof-punch-shape / toast"),
        ((T(5, 40), T(6, 36)), "baker: loaves in / toast"),
        ((T(2, 14), T(3, 58)), "baker: walk-in / whiteboard"),
        ((T(2, 14), T(4, 58)), "baker: walk-in / bread out"),
        ((T(23, 31), T(0, 54)), "baker: mixer three alarms away / empty trays"),
        ((T(23, 31), T(2, 14)), "baker: mixer / walk-in"),
        ((T(0, 54), T(2, 14)), "baker: trays / walk-in"),
        ((T(0, 54), T(3, 58)), "baker: trays / whiteboard"),
        ((T(6, 17), T(7, 17)), "crossing guard arc: vest on chair / takes the corner"),
        ((T(7, 17), T(9, 31)), "crossing guard arc: corner / off-duty coffee"),
        ((T(6, 17), T(9, 31)), "crossing guard arc"),
        ((T(15, 1), T(17, 8)), "crossing guard arc: hand up / vest folded"),
        ((T(7, 18), T(9, 16)), "grandmother arc: dressed early / bank"),
        ((T(19, 40), T(20, 49)), "grandmother arc: ate at five / on the phone"),
        ((T(0, 19), T(1, 29)), "new-father arc: pacing / bottle"),
        ((T(1, 29), T(2, 18)), "new-father arc: bottle / documentary"),
        ((T(0, 19), T(2, 18)), "new-father arc"),
        ((T(2, 18), T(3, 16)), "new-father arc: documentary / swaying"),
        ((T(1, 29), T(3, 16)), "new-father arc"),
        ((T(0, 19), T(3, 16)), "new-father arc"),
        ((T(4, 59), T(5, 22)), "kettle: first to repeat the rumor / butter told to hurry"),
        ((T(0, 39), T(23, 48)), "kettle: cooled two mugs / Tokyo lunchtime"),
        ((T(21, 24), T(23, 53)), "laundry: buzzer ignored / hamper's last argument"),
        ((T(2, 49), T(23, 53)), "laundry: apartment cycle / hamper"),
        ((T(5, 57), T(2, 49)), "laundry: warm towel / apartment dryer (opposite ends of night)"),
        ((T(13, 53), T(16, 41)), "dishwasher: second load / loaded wrong"),
        ((T(16, 41), T(17, 44)), "dishwasher: loaded wrong / still clean and full"),
        ((T(13, 53), T(17, 44)), "dishwasher spread"),
        ((T(17, 44), T(19, 59)), "dishwasher: clean-full / last plate in"),
        ((T(17, 44), T(20, 0)), "dishwasher: clean-full / argument"),
        ((T(2, 11), T(4, 47)), "elsewhere-lunch keeps"),
        ((T(7, 9), T(8, 2)), "school bus: sound two streets over / stop arm"),
        ((T(7, 9), T(8, 43)), "school bus: sound / empty corner"),
        ((T(8, 2), T(8, 43)), "(same-hour)"),
        ((T(14, 40), T(15, 11)), "school bus: staging definition / unloads arguments"),
        ((T(15, 11), T(16, 11)), "school bus: unloads / kid asleep on glass"),
        ((T(14, 40), T(16, 11)), "school bus spread"),
        ((T(3, 7), T(23, 22)), "moth keeps: quota / same argument as last night"),
        ((T(9, 34), T(11, 41)), "pharmacy: gate up / twenty minutes"),
        ((T(0, 2), T(2, 27)), "(retired)"),
        ((T(9, 3), T(10, 14)), "second coffee keeps: decision / focus definition"),
        ((T(9, 3), T(13, 16)), "second coffee / second attempt"),
        ((T(10, 14), T(13, 16)), "coffee keeps"),
        ((T(11, 10), T(13, 16)), "coffee: tar / second attempt"),
        ((T(9, 3), T(11, 10)), "coffee: decision / tar"),
        ((T(10, 14), T(11, 10)), "coffee: focus / tar"),
        ((T(23, 5), T(1, 37)), "sleep-math suite: do not calculate / alarm a suggestion"),
        ((T(23, 36), T(1, 37)), "sleep-math suite"),
        ((T(23, 5), T(1, 4)), "sleep-math suite"),
        ((T(23, 36), T(1, 4)), "sleep-math suite"),
        ((T(23, 5), T(23, 36)), "(same-hour)"),
        ((T(1, 4), T(1, 37)), "(same-hour)"),
        ((T(4, 21), T(2, 36)), "night stocking: bread aisle / floor waxer"),
        ((T(5, 45), T(17, 45)), "quarter-to-six twins"),
        ((T(2, 30), T(14, 30)), "2:30 twins"),
        ((T(0, 15), T(2, 34)), "hospital: reviewed r5, distinct beats"),
        ((T(0, 15), T(2, 7)), "hospital: reviewed r5, distinct beats"),
        ((T(0, 17), T(3, 15)), "refrigerator: reviewed r5, distinct beats"),
        ((T(0, 19), T(22, 17)), "new-father: reviewed r5, distinct beats"),
        ((T(0, 26), T(2, 52)), "highway: reviewed r5, distinct beats"),
        ((T(0, 3), T(22, 17)), "baby: reviewed r5, distinct beats"),
        ((T(0, 31), T(2, 12)), "convenience-store: reviewed r5, distinct beats"),
        ((T(0, 32), T(21, 47)), "porch: reviewed r5, distinct beats"),
        ((T(0, 4), T(2, 33)), "unsent-text: reviewed r5, distinct beats"),
        ((T(1, 12), T(2, 48)), "ceil-fan: reviewed r5, distinct beats"),
        ((T(1, 12), T(23, 33)), "ceil-fan: reviewed r5, distinct beats"),
        ((T(1, 17), T(22, 40)), "second-wind: reviewed r5, distinct beats"),
        ((T(1, 41), T(4, 25)), "airport: reviewed r5, distinct beats"),
        ((T(1, 43), T(3, 55)), "security-guard: reviewed r5, distinct beats"),
        ((T(1, 48), T(23, 44)), "grocery-list: reviewed r5, distinct beats"),
        ((T(10, 10), T(12, 12)), "clock-digit: reviewed r5, distinct beats"),
        ((T(10, 10), T(12, 34)), "clock-digit: reviewed r5, distinct beats"),
        ((T(10, 29), T(13, 22)), "forklift: reviewed r5, distinct beats"),
        ((T(10, 35), T(12, 0)), "sandwich: reviewed r5, distinct beats"),
        ((T(10, 35), T(12, 44)), "sandwich: reviewed r5, distinct beats"),
        ((T(10, 35), T(12, 51)), "sandwich: reviewed r5, distinct beats"),
        ((T(10, 46), T(13, 41)), "load-dock: reviewed r5, distinct beats"),
        ((T(11, 29), T(14, 27)), "school-bell: reviewed r5, distinct beats"),
        ((T(11, 34), T(13, 14)), "office-jargon: reviewed r5, distinct beats"),
        ((T(11, 34), T(13, 47)), "office-jargon: reviewed r5, distinct beats"),
        ((T(11, 34), T(13, 55)), "office-jargon: reviewed r5, distinct beats"),
        ((T(11, 54), T(12, 46)), "soup: reviewed r5, distinct beats"),
        ((T(12, 19), T(14, 43)), "bench: reviewed r5, distinct beats"),
        ((T(12, 24), T(15, 19)), "sign: reviewed r5, distinct beats"),
        ((T(12, 57), T(15, 43)), "pen: reviewed r5, distinct beats"),
        ((T(12, 9), T(13, 0)), "office-fridge: reviewed r5, distinct beats"),
        ((T(13, 41), T(14, 8)), "load-dock: reviewed r5, distinct beats"),
        ((T(13, 41), T(16, 17)), "delivery-truck: reviewed r5, distinct beats"),
        ((T(13, 43), T(15, 37)), "spreadsheet: reviewed r5, distinct beats"),
        ((T(13, 45), T(16, 22)), "onion: reviewed r5, distinct beats"),
        ((T(14, 27), T(15, 0)), "school-bell: reviewed r5, distinct beats"),
        ((T(14, 28), T(16, 30)), "stapler: reviewed r5, distinct beats"),
        ((T(14, 39), T(16, 3)), "classroom: reviewed r5, distinct beats"),
        ((T(14, 44), T(15, 34)), "fold-chair: reviewed r5, distinct beats"),
        ((T(14, 44), T(15, 55)), "gym: reviewed r5, distinct beats"),
        ((T(14, 55), T(15, 26)), "backpack: reviewed r5, distinct beats"),
        ((T(14, 55), T(16, 3)), "classroom: reviewed r5, distinct beats"),
        ((T(14, 55), T(17, 13)), "backpack: reviewed r5, distinct beats"),
        ((T(14, 58), T(17, 41)), "pickup-line: reviewed r5, distinct beats"),
        ((T(14, 58), T(17, 49)), "pickup-line: reviewed r5, distinct beats"),
        ((T(15, 13), T(17, 3)), "grocery-list: reviewed r5, distinct beats"),
        ((T(15, 22), T(16, 50)), "look-busy: reviewed r5, distinct beats"),
        ((T(15, 24), T(16, 36)), "pretzel: reviewed r5, distinct beats"),
        ((T(15, 26), T(17, 13)), "backpack: reviewed r5, distinct beats"),
        ((T(15, 34), T(17, 46)), "fold-chair: reviewed r5, distinct beats"),
        ((T(15, 39), T(18, 14)), "refrigerator: reviewed r5, distinct beats"),
        ((T(15, 5), T(16, 34)), "printer: reviewed r5, distinct beats"),
        ((T(15, 58), T(18, 52)), "recipe: reviewed r5, distinct beats"),
        ((T(15, 8), T(17, 58)), "garage-door: reviewed r5, distinct beats"),
        ((T(16, 22), T(18, 0)), "onion: reviewed r5, distinct beats"),
        ((T(16, 22), T(18, 21)), "onion: reviewed r5, distinct beats"),
        ((T(16, 9), T(17, 0)), "office-chair: reviewed r5, distinct beats"),
        ((T(17, 12), T(19, 0)), "oven: reviewed r5, distinct beats"),
        ((T(17, 12), T(19, 43)), "oven: reviewed r5, distinct beats"),
        ((T(17, 19), T(18, 21)), "pan: reviewed r5, distinct beats"),
        ((T(17, 20), T(18, 25)), "pans: reviewed r5, distinct beats"),
        ((T(17, 39), T(20, 26)), "forklift: reviewed r5, distinct beats"),
        ((T(17, 47), T(18, 29)), "commuter: reviewed r5, distinct beats"),
        ((T(17, 59), T(18, 21)), "pan: reviewed r5, distinct beats"),
        ((T(18, 50), T(19, 19)), "fork: reviewed r5, distinct beats"),
        ((T(18, 52), T(19, 43)), "recipe: reviewed r5, distinct beats"),
        ((T(18, 58), T(19, 49)), "screen-door: reviewed r5, distinct beats"),
        ((T(19, 21), T(21, 37)), "leftover: reviewed r5, distinct beats"),
        ((T(19, 26), T(20, 30)), "dish: reviewed r5, distinct beats"),
        ((T(19, 37), T(21, 36)), "mug: reviewed r5, distinct beats"),
        ((T(19, 38), T(20, 30)), "dish: reviewed r5, distinct beats"),
        ((T(2, 15), T(3, 19)), "intrusive-memory: reviewed r5, distinct beats"),
        ((T(2, 28), T(5, 8)), "gett-up: reviewed r5, distinct beats"),
        ((T(2, 3), T(4, 33)), "red-eye-flight: reviewed r5, distinct beats"),
        ((T(2, 31), T(4, 15)), "truck-stop: reviewed r5, distinct beats"),
        ((T(20, 16), T(21, 47)), "porch: reviewed r5, distinct beats"),
        ((T(20, 25), T(21, 46)), "sleep-kid: reviewed r5, distinct beats"),
        ((T(20, 31), T(21, 9)), "cereal-bowl: reviewed r5, distinct beats"),
        ((T(20, 42), T(22, 53)), "garage: reviewed r5, distinct beats"),
        ((T(20, 5), T(22, 53)), "garage: reviewed r5, distinct beats"),
        ((T(21, 11), T(23, 23)), "nightstand: reviewed r5, distinct beats"),
        ((T(21, 23), T(22, 26)), "gas-station: reviewed r5, distinct beats"),
        ((T(21, 24), T(23, 21)), "dryer: reviewed r5, distinct beats"),
        ((T(21, 25), T(22, 36)), "blanket: reviewed r5, distinct beats"),
        ((T(21, 50), T(22, 38)), "bike: reviewed r5, distinct beats"),
        ((T(3, 15), T(4, 27)), "refrigerator: reviewed r5, distinct beats"),
        ((T(3, 28), T(4, 52)), "third-shift: reviewed r5, distinct beats"),
        ((T(4, 3), T(7, 0)), "sock: reviewed r5, distinct beats"),
        ((T(4, 50), T(5, 16)), "shower: reviewed r5, distinct beats"),
        ((T(4, 50), T(5, 50)), "shower: reviewed r5, distinct beats"),
        ((T(4, 50), T(6, 30)), "shower: reviewed r5, distinct beats"),
        ((T(5, 16), T(6, 30)), "shower: reviewed r5, distinct beats"),
        ((T(5, 20), T(8, 10)), "stairwell: reviewed r5, distinct beats"),
        ((T(5, 25), T(8, 19)), "car-radio: reviewed r5, distinct beats"),
        ((T(5, 27), T(6, 54)), "empty-room: reviewed r5, distinct beats"),
        ((T(5, 50), T(6, 30)), "shower: reviewed r5, distinct beats"),
        ((T(6, 18), T(7, 2)), "pack-lunch: reviewed r5, distinct beats"),
        ((T(6, 34), T(8, 46)), "backpack: reviewed r5, distinct beats"),
        ((T(6, 37), T(9, 34)), "wait-line: reviewed r5, distinct beats"),
        ((T(6, 44), T(7, 13)), "podcast: reviewed r5, distinct beats"),
        ((T(6, 46), T(7, 11)), "banana: reviewed r5, distinct beats"),
        ((T(6, 52), T(7, 29)), "elevator: reviewed r5, distinct beats"),
        ((T(6, 52), T(8, 35)), "elevator: reviewed r5, distinct beats"),
        ((T(6, 59), T(7, 59)), "empty-house: reviewed r5, distinct beats"),
        ((T(7, 29), T(8, 35)), "elevator: reviewed r5, distinct beats"),
        ((T(7, 48), T(8, 56)), "jogger: reviewed r5, distinct beats"),
        ((T(8, 4), T(11, 1)), "bagel: reviewed r5, distinct beats"),
        ((T(8, 9), T(9, 2)), "badge: reviewed r5, distinct beats"),
        ((T(9, 14), T(10, 20)), "mail-carrier: reviewed r5, distinct beats"),
        ((T(9, 14), T(11, 48)), "mail-truck: reviewed r5, distinct beats"),
        ((T(9, 28), T(10, 42)), "roofer: reviewed r5, distinct beats"),
        ((T(9, 4), T(10, 7)), "printer: reviewed r5, distinct beats"),
        ((T(9, 44), T(11, 47)), "new-father: reviewed r5, distinct beats"),
    ]
}

def cdist(i, j):
    d = abs(i - j)
    return min(d, 1440 - d)

bytag = collections.defaultdict(list)
for i, tl in enumerate(ctags):
    for t in tl:
        bytag[t].append(i)

out, suppressed = [], 0
for t, idxs in bytag.items():
    for a, b in itertools.combinations(idxs, 2):
        if a // 60 == b // 60:
            continue
        if cdist(a, b) > 180:
            continue
        if t in TEXTURE or t in SUITES:
            suppressed += 1
            continue
        if tuple(sorted((a, b))) in KEEP_PAIRS:
            continue
        out.append((t, cdist(a, b), a, b))

print(f"IMAGE COLLISIONS (canonical tags, cross-hour, <=180m, minus {len(KEEP_PAIRS)} annotated keeps): {len(out)}")
print(f"pairs suppressed as TEXTURE (reported, not hidden): {suppressed}")
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

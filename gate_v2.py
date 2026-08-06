#!/usr/bin/env python3
"""Session-model duplicate gate. A reader experiences sessions, not the whole
book: pairs close on the clock are held to a much stricter bar than pairs
twelve hours apart. Flags are adjudicated in ADJUDICATION.md."""
import json, re, collections, pathlib, itertools, sys

HOURS = pathlib.Path(__file__).parent / "hours"
poems = [None] * 1440
for h in range(24):
    d = json.loads((HOURS / f"hour_{h:02d}.json").read_text())
    for m, p in enumerate(d["poems"]):
        poems[h * 60 + m] = p

STOP = set("""a an the and or but of to in on at for with from by as is are was were
be been being it its it's this that these those there here not no so if then than
when what who you your i my me we our they their he she his her him them will
would can could do does did have has had one two three out up down off over under
into about just still all some any more most now again very like likes way said
says say goes gets get got going come comes came nobody somebody someone anyone
everyone whoever something anything everything nothing left right back only even
already yet once every each both which where while after before against without""".split())

def stem(w):
    for suf in ("ing", "es", "ed", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: len(w) - len(suf)]
    return w

def cw(p):
    return set(stem(w) for w in re.findall(r"[a-z']+", p.lower())
               if w not in STOP and len(w) > 2)

def g4s(p):
    w = re.findall(r"[a-z']+", p.lower())
    return set(" ".join(w[i:i + 4]) for i in range(len(w) - 3))

# Adjudicated deliberate motifs (see ADJUDICATION.md) — suppressed pairs.
ALLOW = set()
def allow(*mins):
    for a, b in itertools.combinations(mins, 2):
        ALLOW.add(tuple(sorted((a, b))))
T = lambda h, m: h * 60 + m
allow(T(0, 17), T(15, 1))  # like-it-has-been
allow(T(0, 18), T(23, 41))  # overheard found-form, distinct lines
allow(T(0, 18), T(23, 41))  # overheard through the wall
allow(T(0, 24), T(17, 14))  # the dog sighs once, all / brake lights, four lanes, all
allow(T(0, 33), T(19, 35))  # eating from the container: shift / teenager
allow(T(0, 42), T(8, 44))  # lost and found: night / school (mirror)
allow(T(0, 46), T(15, 7))  # granola: stairwell / coat pocket
allow(T(0, 46), T(3, 52))  # break room: stairwell TV / kettle
allow(T(0, 48), T(22, 28))  # blue glow trilogy
allow(T(0, 48), T(23, 39))  # blue glow trilogy
allow(T(0, 50), T(14, 30))  # stopped pretending: night / day (mirror)
allow(T(0, 51), T(7, 11))  # counters: keys / banana
allow(T(0, 7), T(7, 33))  # sinks: cat / mug
allow(T(1, 13), T(17, 2))  # doors propped: shoe / crate / cinder block
allow(T(1, 13), T(5, 28))  # doors propped: shoe / crate / cinder block
allow(T(1, 16), T(20, 15))  # nurses' meals: night / shift start (mirror)
allow(T(1, 28), T(6, 49))  # parking lots: everything closes / church
allow(T(1, 33), T(18, 6))  # next apartment: dishes / chopping
allow(T(1, 34), T(12, 19))  # you-said-you-would keeps (r1)
allow(T(1, 43), T(8, 50))  # parking garage: guard reads / radios mid-chorus (7h apart)
allow(T(1, 46), T(9, 0))  # confidence-of: futon / nine o'clock
allow(T(1, 48), T(15, 13))  # the grocery list, traveling (arc)
allow(T(1, 50), T(15, 2))  # ten to two. somewhere a / 3:02. the meeting could have
allow(T(10, 13), T(17, 17))  # meetings: email / new business (r1 keeps)
allow(T(10, 18), T(16, 21))  # never-once family
allow(T(10, 18), T(17, 42))  # not-in-a-hurry: retired man / food cart
allow(T(10, 54), T(20, 35))  # somebody's mother is on speakerphone / somebody in this house has
allow(T(10, 6), T(14, 2))  # nurse charting arc (5 kept)
allow(T(10, 6), T(14, 2))  # nurse charting the time
allow(T(11, 24), T(15, 18))  # dog let out / dog staring (different jokes)
allow(T(11, 25), T(16, 40))  # the avoided email, an arc
allow(T(11, 26), T(14, 43))  # benches: library / dialysis
allow(T(11, 6), T(23, 39))  # what was going to be / blue glow on a face
allow(T(12, 12), T(14, 9))  # day-shape: typo minute / afternoon definition
allow(T(12, 13), T(22, 12))  # that-is-the-whole: argument / ceremony
allow(T(12, 21), T(17, 10))  # by-a-person-who: salad / rush hour
allow(T(12, 26), T(22, 14))  # somebody's mother: weekday call / helped to bed
allow(T(12, 40), T(21, 4))  # reached-the-volume: cafeteria / bar (mirror)
allow(T(13, 13), T(16, 45))  # alarms: nobody admits / shift at five
allow(T(13, 19), T(20, 39))  # the-one-thing-that: mail / label
allow(T(13, 53), T(20, 0))  # dishwasher: second load (13:53) / argument — distant, distinct
allow(T(14, 24), T(15, 24))  # good ideas: never at 2:24 / apple
allow(T(14, 48), T(19, 48))  # you will not remember 2:48 / the table cleared to where
allow(T(15, 10), T(20, 37))  # deciding: the day / tomorrow
allow(T(15, 5), T(16, 52))  # 'asked to do a': copier / minute
allow(T(16, 17), T(21, 54))  # engines off: UPS / driveway song
allow(T(16, 20), T(20, 55))  # definitions: quitting time / bedtime
allow(T(16, 26), T(23, 40))  # hospital carts: arguing wheel / bad wheel (night reprise)
allow(T(16, 48), T(20, 49))  # has-been-on: homework / grandmother's call
allow(T(18, 41), T(20, 15))  # eats standing: doesn't count / counts (mirror)
allow(T(19, 41), T(21, 19))  # phone battles, distinct jokes
allow(T(2, 0), T(10, 25))  # court in session: 2 a.m. / docket of Tuesdays (reprise)
allow(T(2, 1), T(10, 25))  # is-a-list-of family
allow(T(2, 1), T(6, 40))  # is-a-list-of family
allow(T(2, 10), T(23, 41))  # 'then nothing': motion light / argument
allow(T(2, 14), T(11, 7))  # walk-in: dough / tomatoes (trade texture)
allow(T(2, 22), T(22, 30))  # last bus keeps
allow(T(2, 22), T(6, 26))  # night's edges
allow(T(2, 26), T(23, 37))  # the cat has business (night motif)
allow(T(2, 30), T(11, 47))  # exact middles
allow(T(2, 30), T(14, 30))  # the 2:30 twins (same-minute mirror)
allow(T(2, 34), T(8, 46))  # ER doors / train doors
allow(T(2, 4), T(14, 12))  # instruction found-forms, distinct
allow(T(2, 47), T(16, 19))  # sandwiches: tow cab / break room
allow(T(2, 50), T(19, 4))  # bottoms
allow(T(2, 58), T(10, 18))  # never-once family
allow(T(2, 58), T(16, 21))  # never-once family
allow(T(21, 19), T(23, 57))  # phone battles, distinct jokes
allow(T(22, 28), T(23, 39))  # blue glow trilogy
allow(T(3, 26), T(6, 30))  # opinions: cat / top floor
allow(T(3, 43), T(14, 48))  # you will not remember
allow(T(3, 43), T(9, 38))  # you will not remember
allow(T(3, 50), T(17, 24))  # folded against walls: wheelchair / stroller (mirror)
allow(T(3, 55), T(17, 9))  # the security guard walks the / a woman crosses the parking
allow(T(3, 58), T(17, 57))  # grease pencils: bake board / specials board (mirror)
allow(T(4, 19), T(13, 18))  # the white truck idles at / 1:18. eyes at the end
allow(T(4, 31), T(6, 41))  # overheard found-form, distinct lines
allow(T(4, 59), T(9, 9))  # day as rumor / plan still perfect
allow(T(4, 6), T(21, 13))  # dog-decided trilogy
allow(T(4, 6), T(7, 3))  # dog-decided trilogy
allow(T(4, 9), T(22, 17))  # baby finally down: nobody moves / forty minutes (mirror)
allow(T(5, 12), T(14, 48))  # thirty days. the chip is / you will not remember 2:48
allow(T(5, 12), T(19, 48))  # thirty days. the chip is / the table cleared to where
allow(T(5, 14), T(8, 38))  # reflective vests: waiting / waving (thread)
allow(T(5, 20), T(8, 10))  # overheard found-form, distinct lines
allow(T(5, 27), T(6, 54))  # empty rooms: reps / alarm
allow(T(5, 28), T(17, 2))  # doors propped: shoe / crate / cinder block
allow(T(5, 38), T(17, 0))  # the kid with swim practice / 5:00. the chair is still
allow(T(5, 39), T(9, 24))  # nutrition labels
allow(T(5, 55), T(9, 5))  # five minutes: anything / late personality
allow(T(5, 6), T(23, 54))  # nurse charting arc (5 kept)
allow(T(5, 9), T(22, 12))  # the bulb over the range: morning / night (mirror)
allow(T(6, 10), T(16, 59))  # at 6:10 the bus is / 4:59, which is not five,
allow(T(6, 23), T(18, 5))  # inside-of: windshield ice / kitchen steam
allow(T(6, 34), T(8, 46))  # backpack straps: chewed / train door
allow(T(6, 35), T(20, 41))  # other time zones (core theme)
allow(T(6, 45), T(20, 35))  # whoever is going to be / somebody in this house has
allow(T(6, 54), T(7, 35))  # alarms: empty room / fourth time
allow(T(7, 18), T(20, 49))  # grandmothers, spread
allow(T(7, 24), T(15, 38))  # truck lunches (thread)
allow(T(7, 3), T(21, 13))  # dog-decided trilogy
allow(T(7, 32), T(18, 47))  # with-nobody-in-it: car / house
allow(T(7, 35), T(16, 45))  # alarms (r1 keeps)
allow(T(7, 44), T(10, 54))  # parking lots: name tag / speakerphone
allow(T(7, 7), T(13, 25))  # nobody-has-said: true yet / four minutes
allow(T(8, 35), T(13, 43))  # agreeing to look: elevator / spreadsheet
allow(T(8, 42), T(18, 26))  # it-will-not-be: optimism / smoke alarm
allow(T(8, 46), T(17, 23))  # train doors: strap / coat sleeve (commute mirror)
allow(T(8, 54), T(16, 19))  # labeled-food keeps
allow(T(8, 9), T(12, 46))  # it-has-always-been: coat / soup
allow(T(9, 21), T(17, 25))  # whatever-you-were-going: morning / evening (mirror)
allow(T(9, 32), T(21, 46))  # asleep-on: dog couch / kid floor
allow(T(9, 38), T(14, 48))  # you will not remember
allow(T(9, 59), T(22, 17))  # 9:59. the meeting ends four / 10:17 and the baby is
allow(T(9, 6), T(10, 6))  # nurse charting arc (5 kept)
allow(T(9, 6), T(10, 6))  # nurse charting the time
allow(T(9, 6), T(14, 2))  # nurse charting arc (5 kept)
allow(T(9, 6), T(14, 2))  # nurse charting the time
allow(T(9, 9), T(13, 9))  # the plan's decay, an arc

allow(T(9, 19), T(9, 40))    # school-day family, same hour: missed-bus victor / long division elsewhere-benign
allow(T(9, 40), T(12, 40))   # school-day family, farthest members: long division / cafeteria volume
allow(T(7, 24), T(8, 0))     # working men: sandwich steered with a knee / Corolla merging on faith
allow(T(8, 0), T(8, 38))     # working men: Corolla on faith / vest waving the truck back, unhurried
allow(T(7, 24), T(8, 38))    # working men: knee-steered sandwich / two-finger truck wave
allow(T(5, 14), T(7, 24))    # working men: vest waiting at an empty crosswalk / sandwich at the wheel
allow(T(5, 14), T(8, 0))     # working men: empty-crosswalk patience / merging on faith
allow(T(13, 17), T(15, 38))  # working men: hard hat asleep, boots on dash / lunch at 3:38 because the job allowed it
allow(T(15, 38), T(17, 29))  # working men: lunch when the job let him / suit jacket, lottery ticket and a banana
allow(T(12, 47), T(13, 51))  # working women: rotisserie chicken across the lot / barcode gun chirping yes
allow(T(7, 56), T(9, 31))    # parked cars: key not turned yet / guard's off-duty coffee (also an image-gate keep)
allow(T(1, 0), T(1, 56))     # last-of-the, same hour: the floor drain takes the day / the ice melts and the shift ends

# recurring-cast phrases: threads and found-form families, adjudicated
PHRASE_ALLOW = {"a man in a", "a woman in a", "a woman on a",
                "if it is a", "it is a school", "is a school day", "a school day the",
                "the last of the", "in the break room", "in a parked car",
                "the size of a", "and will not be", "has decided this is",
                "who will not be", "do not open the",
                "thank you come again", "in the lost and", "part of the day",
                "the part of the"}

C = [cw(p) for p in poems]
G = [g4s(p) for p in poems]
def cdist(i, j):
    d = abs(i - j)
    return min(d, 1440 - d)

flags = {}
ALLOW_HIT = set()
ALLOWED_FLAGS = {}
PHRASE_HIT = collections.Counter()
def add(i, j, why):
    k = tuple(sorted((i, j)))
    if k in ALLOW:
        ALLOW_HIT.add(k)
        ALLOWED_FLAGS.setdefault(k, []).append(why)
        return
    flags.setdefault(k, []).append(why)

for i in range(1440):
    for j in range(i + 1, 1440):
        d0 = cdist(i, j)
        removed = G[i] & G[j] & PHRASE_ALLOW if d0 > 180 else set()
        for ph in removed:
            PHRASE_HIT[ph] += 1
        shared4 = (G[i] & G[j]) - removed
        if shared4:
            add(i, j, f"4gram:'{sorted(shared4)[0]}'")
        inter = C[i] & C[j]
        if len(inter) < 2:
            continue
        jac = len(inter) / len(C[i] | C[j])
        d = cdist(i, j)
        if d <= 180 and (jac >= 0.30 or len(inter) >= 4):
            add(i, j, f"near jac={jac:.2f} inter={len(inter)}")
        elif d <= 360 and (jac >= 0.40 or len(inter) >= 5):
            add(i, j, f"mid jac={jac:.2f} inter={len(inter)}")
        elif jac >= 0.50:
            add(i, j, f"far jac={jac:.2f}")

# rare distinctive word co-occurring inside a session window
wordmap = collections.defaultdict(list)
for i, c in enumerate(C):
    for w in c:
        if len(w) >= 6:
            wordmap[w].append(i)
for w, idxs in wordmap.items():
    if 2 <= len(idxs) <= 3:
        for i, j in itertools.combinations(idxs, 2):
            if cdist(i, j) <= 120:
                add(i, j, f"rareword:'{w}'")

def is_priority(whys, d):
    return any("4gram" in w for w in whys) or (d <= 180 and any(
        re.search(r"jac=0\.[4-9]", w) for w in whys))
prio = {k: v for k, v in flags.items() if is_priority(v, cdist(*k))}
prio_allowed = {k: v for k, v in ALLOWED_FLAGS.items() if is_priority(v, cdist(*k))}
print(f"FLAGGED PAIRS: {len(flags)}  PRIORITY after allows: {len(prio)}  "
      f"(priority-class pairs inside ALLOW, suppressed with reasons: {len(prio_allowed)})")
print(f"ALLOW entries: {len(ALLOW)}; consulted this run: {len(ALLOW_HIT)}; never consulted (prune): {len(ALLOW - ALLOW_HIT)}")
dead_ph = [ph for ph in PHRASE_ALLOW if PHRASE_HIT[ph] == 0]
print(f"PHRASE_ALLOW entries: {len(PHRASE_ALLOW)} (suppress OUT-of-window only; in-window shared phrases flag normally); out-of-window co-occurrence count per entry: "
      + ", ".join(f"'{ph}':{PHRASE_HIT[ph]}" for ph in sorted(PHRASE_ALLOW)) )
print(f"PHRASE_ALLOW never consulted (prune): {len(dead_ph)} {sorted(dead_ph)}")
for (i, j), whys in sorted(flags.items(), key=lambda x: cdist(*x[0])):
    print(f"[{i//60:02d}:{i%60:02d}]~[{j//60:02d}:{j%60:02d}] d={cdist(i,j)}m  {'; '.join(whys[:2])}")
    print(f"   A: {poems[i][:72].replace(chr(10), ' / ')}")
    print(f"   B: {poems[j][:72].replace(chr(10), ' / ')}")

print("\nSHORT-POEM QUOTA (need >=10 of <=8 words per hour):")
for h in range(24):
    n = sum(1 for m in range(60) if len(poems[h * 60 + m].split()) <= 8)
    print(f"  hour {h:02d}: {n}" + ("  MISS" if n < 10 else ""))

# Repetition Adjudication — working record

A reader experiences sessions, not the whole book: whoever is awake at 8 p.m.
is awake at 9 p.m. The invariant: **no image or joke appears twice inside a
180-minute circular window from different hours without an entry here.**
Same-hour repeats are one author's deliberate sequencing and are exempt.

## Instruments (all must pass before a build ships)

- `image_gate.py` — the primary check (Destroyer r3's prescription). Every
  poem carries 1–3 image tags (`hours_tags/`, written by a model pass, updated
  by hand with every edit). Flags any specific tag shared across hours within
  the window, minus the keep-pairs listed in the script. Generic families
  (bar, meeting, dishwasher, school-bus…) are density-adjudicated below, not
  pairwise. Current state: **0 collisions.**
- `gate_v2.py` — lexical screen: session-weighted stemmed Jaccard, cross-hour
  4-grams, rare-word co-occurrence, and the ≤8-words-per-hour quota
  (BRIEF.md's only machine-checkable quota that had failed; the other quotas —
  minute-naming, direct address, rationed words, found-forms — were verified
  by hand and by Destroyer r3's independent counts). Current state: 0
  priority flags, 0 quota misses; two far 4-grams pinned ("in the parking
  garage", "on the parking lot" — different beats, different hours).
- Neither gate certifies quality; they certify the absence of the failure
  classes three Destroyer rounds actually found. The image tags are
  themselves a model artifact and can mislabel; the tag pass is re-run on
  edited poems by hand.

## Family curation (what "one per window" left standing)

Dishwasher 6 beats spread 13:53–01:10 (was 9) · bath 3 (was 4, plus the towel
fossil) · moths 2, at 03:07 and 23:22 (was 7) · vending machines 2 (was 6) ·
ice machines 2, house night + hospital (was 4) · alarms: the pre-dawn suite,
each a distinct joke · bar: seven distinct beats across 16:27–01:05 ·
practice pickup 3 (was 7) · trash-to-curb 1 (was 6) · crossing guard 5-beat
day arc (was 8) · grandmother 5-beat day arc (was 7) · new-father night arc
00:19 → 11:47, one beat per scene · nurse charting 5, spaced · microwaved
fish 1 (was 3) · printer 2 (was 3) · copier 2 (was 4) · drafted-and-deleted
text 1 (was 3) · rooster 1 (was 2) · kettles 4 spread across the day (was 6).

## Deliberate structures (not defects)

- Arcs: the avoided email (05:16→16:40) · the plan's decay (09:09→15:57) ·
  the traveling grocery list (01:48, 15:13) · the insomnia-arithmetic suite
  (23:05, 23:36, 01:04, 01:37 — two per hour, author-paired) · onions bought
  → in the pan → skin by the trash (16:22, 18:00, 18:21, 19:12)
- Recurring cast: the dog (outvoted / sunbeam / bedtime), the nurses, the
  working men and women vignettes, the cat with business
- Motifs: blue glow escalating (00:48, 22:28, 23:39) · "you will not
  remember" (03:43, 09:38, 14:48) · overheard through walls and floors, each
  a different line · court in session (02:00, reprised 10:25) · same-minute
  twins (02:30/14:30, 05:45/17:45) · receipts (2 keep THANK YOU COME AGAIN,
  now 8+ hours apart; 4 variant closers)
- Accidental sequences kept because they read as intended: "The last plate
  goes in" → "The dishwasher starts its long argument" (19:59→20:00); the
  hour-5 baker writes "in the oven by 5:40" and the 5:40 poem is the loaves
  going in.

## History

- R1 (HIGH, conceded): per-hour QA blind across hours → 81 rewrites, first
  cross-hour gates.
- R2 (REDESIGN SIGNAL, conceded): thresholds had been fitted around known
  clusters → session-model lexical gate, 108 rewrites, this file created.
- R3 (CRITICAL + REDESIGN SIGNAL, conceded): lexical overlap cannot see a
  repeated image; the allowlist waived all bars at once; hour-22 quota miss;
  19:45 daylight violation → full image-tag pass over all 1,440, ~110 more
  rewrites adjudicated at image level, image_gate.py as primary instrument,
  quota machine-checked, keep-pairs annotated with reasons.

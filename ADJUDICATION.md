# Repetition Adjudication — working record

A reader experiences sessions, not the whole book. The invariant: **no image
or joke appears twice inside a 180-minute circular window from different hours
without an entry in a gate's keep list or a suite below.** Same-hour repeats
are one author's deliberate sequencing and are exempt from the pair check.

## Instruments (all run before any build ships; nothing suppressed silently)

- `image_gate.py` v3 — canonical-vocabulary image check. Tags (hours_tags/,
  one per poem from a model pass, hand-updated with every edit) are mapped
  through a SYNONYMS table so granularity variants collide (trash-bag /
  recycling-bin / dumpster → trash). Pair check runs on everything except a
  named TEXTURE list (furniture words) and the SUITES below; both suppression
  volumes are printed with every run, and suite membership is printed
  minute-by-minute. Keep-pairs carry per-pair reasons and are checked before
  any exemption. Current: **0 collisions · 1,113 texture pairs suppressed
  (reported) · 231 annotated keeps.**
- `gate_v2.py` — lexical screen (session-weighted stemmed Jaccard, cross-hour
  4-grams, rare-word co-occurrence, short-poem quota). Current: 0 priority
  flags, 0 quota misses.
- Density report: every canonical tag, max instances in any 90-minute window
  spanning 2+ hours; >3 prints as a flag. Current flags, adjudicated below:
  baker 5x (the pre-dawn chorus), bar 4x (of which two beats are exterior).
- BRIEF.md's found-form quotas *require* many list/instruction/receipt/
  overheard poems (>=4 per hour by design); forms are exempt from density but
  their contents are pair-checked lexically. The self-referential
  minute-itself poems are the book's spine and exempt as a class.
- Limits, stated plainly: the tags are a model artifact; free-text granularity
  bounds recall even after canonicalization, and no inter-rater measurement
  exists. The gates certify the absence of the failure classes four Destroyer
  rounds found, not the absence of all repetition.

## Suites — documented choruses (member lists print from image_gate.py)

Counts below are the gate's own output, not memory: alarm 13 (the night's
percussion; snooze-label/definition pair and waiting-alarm pair were cut) ·
baker 16 (the pre-dawn trade, incl. the 5:17→5:40 deliberate cross-reference)
· bar 15 across 16:27–01:50 (hour 21 cut from five interior beats to two;
current worst window is four beats of which two are exterior) · city-bus 14
(school-bus is a separate tag) · email 8 + inbox 1 (the white-collar
bloodstream; the twin midnight-email jokes and two staleness jokes were cut)
· homework 5 (was 8) · meeting 10 · nurse 18 (hospital night runs on them) ·
overheard 33 (each a different line — the found-form quota at work) ·
sleep-math 4 (author-paired at both ends of the night) · to-do-list 6 (the
plan's decay) · trash 8 (post-cull: instruction, mop-run, raccoon, tipped bin,
jogger's landmark, last bite, pizza box, dumpster backdrop — one bin-to-curb
poem remains) · couple 4 · minute-itself 22.

## Arcs, cast, mirrors (unchanged from r3, verified still present)

The avoided email · the plan's decay · the traveling grocery list · onions
bought→pan→skin · dog trilogy · blue-glow escalation · "you will not
remember" x3 · court in session reprised · same-minute twins (02:30/14:30,
05:45/17:45) · crossing-guard and grandmother day arcs · new-father night arc
· nurse charting arc · accidental sequences kept as intended (19:59→20:00).

## History

- R1 (HIGH): per-hour QA blind across hours → 81 rewrites, first gates.
- R2 (REDESIGN): thresholds fitted around known clusters → session-model
  lexical gate, 108 rewrites.
- R3 (CRITICAL + REDESIGN): lexical overlap can't see images → full tag pass,
  image gate, ~130 rewrites.
- R4 (CRITICAL + 2 HIGH + REDESIGN): the GENERIC exemption hid the r3
  families and made the keep annotations unreachable; family counts in this
  file were wrong; free-text tag granularity blinds exact matching. →
  Exemption list replaced by printed TEXTURE + SUITES with reasons;
  canonicalized vocabulary; keeps checked first; suppression volumes and
  suite membership printed every run; ~30 further rewrites (practice 6→3,
  evening trash-out →1, hour-21 bar 5→2, alarm/email/homework/shower trims,
  plus my own insertions the honest gates caught). This file's numbers now
  come from the gate's output, not from memory.

# Repetition Adjudication — working record

A reader experiences sessions, not the whole book. The invariant: **no image
or joke appears twice inside a 180-minute circular window from different hours
without an entry in a gate's keep list or a suite below.** Same-hour repeats
are exempt from the pair check but printed in full and read (see next
section) — the sequencing assumption is verified, not presumed.

## Same-hour repeats (policy revised, r5)

The "one author's deliberate sequencing" assumption was tested empirically in
r5: the gate now prints every same-hour identical-tag pair with excerpts (94
currently), and the full list was read end to end. It was not all deliberate —
30 pairs were the same joke twice (shopping carts six minutes apart, two
aprons, two deli-number jokes, twin pillows, twin day-verdicts, the window
washer twice in four minutes) and were rewritten. What remains reads as
development or form-contrast on inspection; the printed list makes every
future edit re-checkable.

## Instruments (all run before any build ships; nothing suppressed silently)

- `image_gate.py` v3 — canonical-vocabulary image check. Tags (hours_tags/,
  one per poem from a model pass, hand-updated with every edit) are mapped
  through a SYNONYMS table so granularity variants collide (trash-bag /
  recycling-bin / dumpster → trash). Pair check runs on everything except a
  named TEXTURE list (furniture words) and the SUITES below; both suppression
  volumes are printed with every run, and suite membership is printed
  minute-by-minute. Keep-pairs carry per-pair reasons and are checked before
  any exemption, with applied and never-consulted keeps counted separately;
  every reason names both beats, derived from the two poems' own divergent
  tags (pairs whose beats could not be distinguished were rewritten: the
  office-jargon cluster, the wait-before-open pair, the copier-animal, the
  afternoon-slump twins). Current: **0 collisions · 142 keeps, all firing,
  0 decorative · 1,123 suppressed pairs, all counted in the output.**
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

## The stated decision (r6 close-out)

Six Destroyer rounds, ~360 adjudicated rewrites, three generations of
instrument. Round 6's verdict named the honest exits: semantic
nearest-neighbour scoring, or a stated and accepted decision that the corpus
ships with a residual repetition rate no tag or lexical instrument can
measure. This is that statement.

What is measured and clean: verbatim and near-verbatim duplication, shared
distinctive phrasing, same-image collisions under a canonicalized vocabulary
within reading windows, family density, and every specific class six rounds
of adversarial review surfaced — each fixed and gated. What is not
measurable with these instruments: semantic convergence with disjoint
vocabulary and disjoint tags, and shared syntax templates. Those classes have
been reduced only by end-to-end reads (the whole corpus has now been read in
reading order across rounds 3–6) and by the gates' printed reports, not
eliminated by proof.

The decision: the book ships with that residual. In a 1,440-poem book written
in one voice about one ordinary day, what remains at this level — a dog seen
many times, kitchens that behave like kitchens — is the texture of a
single-author collection, not a defect class. The dog is now a documented
suite (30 members, five same-joke pairs cut in r6), as are the other
recurring presences; every suppression the instruments make is printed with
membership or per-member counts; nothing is exempt silently. Anyone auditing
the book starts from the same reports the author used.

## History

- R1 (HIGH): per-hour QA blind across hours → 81 rewrites, first gates.
- R2 (REDESIGN): thresholds fitted around known clusters → session-model
  lexical gate, 108 rewrites.
- R3 (CRITICAL + REDESIGN): lexical overlap can't see images → full tag pass,
  image gate, ~130 rewrites.
- R6 (CRITICAL + 2 HIGH + REDESIGN): the dog — the book's most frequent
  character — sat in TEXTURE, unchecked and undocumented, with five same-joke
  pairs; the bulb-left-on triple was invisible because three taggers chose
  three labels; TEXTURE held scene words; regenerated reasons included
  form-shaped boilerplate. → Dog/cat/left-on-light canonicalized and moved to
  printed suites with 6 rewrites; TEXTURE cut to true furniture with a
  per-member suppression report (count + closest pair) printed every run;
  themes and places demoted from texture to printed suites; cited reasons
  rewritten to name beats in words; the stated decision above adopted in
  place of a seventh threshold pass.
- R5 (CRITICAL + 3 HIGH + 1 MEDIUM + REDESIGN): the same-hour exemption was
  untested; keeps were STILL consulted after exemptions; 113 boilerplate
  reasons; plan-arc vocabulary fragmented; syntax templates invisible to both
  gates. → Same-hour list printed and read (30 rewrites), ordering actually
  fixed with hit-counting, reasons regenerated to name beats, plan/sleep-math
  canonicalized, the pharmacy/agenda template pair cut. Known open limit:
  no gate sees shared syntax; that class is only covered by end-to-end reads.
- R4 (CRITICAL + 2 HIGH + REDESIGN): the GENERIC exemption hid the r3
  families and made the keep annotations unreachable; family counts in this
  file were wrong; free-text tag granularity blinds exact matching. →
  Exemption list replaced by printed TEXTURE + SUITES with reasons;
  canonicalized vocabulary; keeps checked first; suppression volumes and
  suite membership printed every run; ~30 further rewrites (practice 6→3,
  evening trash-out →1, hour-21 bar 5→2, alarm/email/homework/shower trims,
  plus my own insertions the honest gates caught). This file's numbers now
  come from the gate's output, not from memory.

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

## Suites — every pair-check exemption, documented (counts print from image_gate.py)

A suite is a deliberate acceptance: identical-tag pairs inside these families
are NOT checked pairwise, because recurrence is the family's nature. That is a
choice, not an instrument limit, and this list is exhaustive — a tag is either
specific (pair-checked), a suite below, or furniture (TEXTURE, with a
per-member suppression report printed every run). Same-joke pairs inside
suites were hunted by the density report and by end-to-end reads in rounds
3–7 (dog 29→24 after five same-joke cuts; bulb-family 6→4 with the two
surviving window pairs entered as named keeps and the family returned to the
pair check in r7).

Characters — a day contains them repeatedly by design: dog 24 · cat 14 ·
nurse 18 · baker 16 · night-shift 12 · teenager 7 · new-father 7 ·
grandmother 5 · mother 5 · couple 4.

Places and their traffic — where the day happens: bar 15 · city-bus 14 ·
park-lot 13 · truck 9 · radio 7 · trash 7 · warehouse 6 · park-car 5.

Hour-themes — the brief's own arc assigns them: minute-itself 22 · alarm 13 ·
plan 12 · meeting 11 · time-zone 11 · sleep-math 9 · email 8 + inbox 1 ·
argument 8 · phone-call 7 · homework 5 · hunger 5 · procrastination 5 ·
wait 5 · regret 4 · text-message 4 · bedtime 3 · insomnia 3 · latenes 3 ·
neighbor 3 · routine 2.

Forms — BRIEF.md mandates ≥4 found-forms per hour, so their volume is the
quota working: list-form 48 · instruction-form 37 · overheard 32 ·
definition-form 28 · receipt-form 12.

## Arcs, cast, mirrors (unchanged from r3, verified still present)

The avoided email · the plan's decay · the traveling grocery list · onions
bought→pan→skin · dog trilogy · blue-glow escalation · "you will not
remember" x3 · court in session reprised · same-minute twins (02:30/14:30,
05:45/17:45) · crossing-guard and grandmother day arcs · new-father night arc
· nurse charting arc · accidental sequences kept as intended (19:59→20:00).

## The stated decision (r7-corrected)

Round 7 rejected the first draft of this decision for conflating two different
things, and it was right: a residual the instruments *cannot see* and a
residual the instruments are *told to ignore* are not the same. Both exist
here, and this statement now names each.

Told to ignore, on the record: the suites above. For those families, in-window
recurrence is accepted as the book's texture, family by family, with counts
printed every run and same-joke pairs inside them cut whenever a round's read
found one (most recently the bulb pair across midnight and five dog pairs).
Anything not in the suite list or TEXTURE is pair-checked; keeps carry reasons
that name both beats; keeps that stop firing are pruned, not kept as
decoration.

Cannot see, stated plainly: semantic convergence with disjoint vocabulary and
disjoint tags, and shared syntax templates. Those classes were reduced only by
reading — the corpus has been read end to end across rounds 3–7 — and are not
eliminated by proof. No tag or lexical instrument here measures them; a
semantic nearest-neighbour pass is the known better instrument and was not
built.

The decision: the book ships with both residuals as bounded above. In a
1,440-poem book in one voice about one ordinary day, the accepted texture — a
dog seen two dozen times, bars that fill at night, alarms that go off at dawn
— is the fabric of the form. Anyone auditing the book starts from the same
printed reports and this record.

## History

- R1 (HIGH): per-hour QA blind across hours → 81 rewrites, first gates.
- R2 (REDESIGN): thresholds fitted around known clusters → session-model
  lexical gate, 108 rewrites.
- R3 (CRITICAL + REDESIGN): lexical overlap can't see images → full tag pass,
  image gate, ~130 rewrites.
- R7 (CRITICAL + 2 HIGH + 1 MEDIUM + REDESIGN): the r6 light-canonicalization
  routed straight into SUITES, suppressing the very class it claimed to fix
  (one-light-for-nobody shipped twice, 73 minutes across midnight); SUITES
  held 30 undocumented tags against an in-code claim of documentation;
  form-shaped keep reasons persisted; one granularity variant unmapped. →
  Bulb pair cut, 20:03's porch-light line rewritten, the ritual variant
  mapped, left-on-light returned to the pair check with named keeps; every
  suite now documented with its count and basis (see roster above); the two
  dead keeps pruned; the eight remaining form-shaped reasons rewritten as
  beats; the decision itself rewritten to distinguish told-to-ignore from
  cannot-see.
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

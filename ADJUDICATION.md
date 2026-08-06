# Repetition Adjudication — working record

A reader experiences sessions, not the whole book. The invariant: **no image
or joke appears twice inside a 180-minute circular window from different hours
without an entry in a gate's keep list or a suite below.** Same-hour repeats
are exempt from the pair check but printed in full and read (see next
section) — the sequencing assumption is verified, not presumed.

## Same-hour repeats (third told-to-ignore class, named as such in r8)

Same-hour pairs are exempt from the pair check by rule — the third
told-to-ignore class alongside suites and texture; the decision below names
all three. The control is a printed list plus reads on the record: the gate
prints every same-hour identical-tag pair with excerpts. Read end-to-end at
94 pairs in r5 (30 same-joke rewrites) and again at 213 pairs in r8 after the
suite tags joined the list (one further cut: the "Still open:" twin across
midnight; the 02:25/02:40 tire-list echo kept as the insomniac mind's
deliberate escalation). Future edits re-print the list.

## Instruments — per-instrument scope and live output (r8 discipline)

Each instrument's own printed output is the source for every number here; both
gates now carry the same discipline (computed classifications, printed
suppression volumes, consultation-counted allow lists).

- `image_gate.py` — canonical-vocabulary image check. Live output: 0
  collisions · 146 keeps, all firing, 0 decorative · 1,104 suppressed pairs
  counted in the output · per-TEXTURE-member suppression report with the
  closest pair sampled · suite membership printed minute-by-minute ·
  same-hour list printed in full.
- `gate_v2.py` — lexical screen. The "priority" classification (a 4-gram
  anywhere, or a within-window Jaccard >= 0.40) is computed and printed by
  the gate itself as of r8, not applied downstream. Live output: 104 raw
  flags · 0 priority · 115 allow entries, all consulted, 0 never-consulted ·
  0 quota misses. The 104 sub-priority flags are mid/far-window moderate
  overlaps and rare-word co-occurrences; the within-window subset was
  reviewed in rounds 2–5 and the acted-on bar is the printed priority line.
- Density report: every canonical tag, max instances in any 90-minute window
  spanning 2+ hours; >3 prints. Current flags, adjudicated: baker 5x (the
  pre-dawn chorus), bar 4x (two of the four beats exterior).
- Limits, stated plainly: the tags are a model artifact with no inter-rater
  measurement; canonicalization closes label variants only when mapped; the
  gates certify the absence of the failure classes eight Destroyer rounds
  surfaced, not the absence of all repetition.

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

Told to ignore, on the record — three classes: (1) the suites above; (2)
same-hour pairs, printed in full and read on the record; (3) TEXTURE
furniture words, with per-member suppression counts and closest pairs
printed. For those families, in-window
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
- R8 (CRITICAL + HIGH + 3 MEDIUM + REDESIGN): the record described
  image_gate's discipline as "the gates'" while gate_v2 carried a downstream
  "priority" number it never computed, ~100 dead allow entries (two citing
  poems r7 had deleted), and seventeen unreasoned suppressions; same-hour was
  an unnamed third told-to-ignore class anchored to a stale 94-pair read;
  headline numbers were stale; the bulb census was wrong; the "Still open:"
  twin crossed midnight inside the list-form suite. → gate_v2 instrumented to
  compute priority and count allow consultations; allow list regenerated to
  the 115 firing entries with named beats; the twin cut; street-lamp variants
  canonicalized with named keeps; the 213-pair same-hour list re-read on the
  record; this file re-synced to the instruments' live output; the decision
  now names three told-to-ignore classes.
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

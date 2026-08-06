# EVERY MINUTE — Master Brief

## The work

1,440 poems, one for every minute of the day. A website shows only the poem for
the current minute, in the reader's local time zone. No archive, no browsing.
Each poem is, for one minute a day, the entire book. Some poems (3:41 a.m.) may
go unread for months. The book can never be read cover to cover by anyone.

You are writing the 60 poems for ONE assigned hour. The poem at index M is the
poem for HH:MM. It appears at that minute every day, forever — weekday and
weekend, January and July.

## Hard constraints

1. **Every-day truth.** Your poem shows at its minute in every season. Do not
   assert things false half the year: no "snow falling," no "golden hour" pinned
   to a clock time, no fixed sunrise/sunset claims. Night hours (22:00–04:59)
   are safely dark; 05:00–07:59 and 16:00–20:59 have variable light — hedge
   gracefully ("somewhere it is already light") or stay off daylight entirely.
   Weekday-specific claims must hedge too ("if it's Monday...").
2. **Length.** Nothing over 40 words. Median under 18 words. Some poems are two
   or three words.
3. **No titles, no numbering, no meta.** Never use the word "poem." Never
   explain the poem. Never address the project itself.
4. **No em-dashes.** Commas, periods, line breaks.

## Form quotas (per your 60)

- ≥ 10 poems of 8 words or fewer
- ≥ 5 that are a single observed object or scene, no commentary at all
- ≥ 5 with dry humor (wit, not jokes)
- ≥ 4 "found forms": a list, a definition, an instruction, an overheard
  sentence, a fragment of a receipt/form/label
- ≥ 6 that name their exact minute in the text ("3:41," "at 3:41 a.m.")
- ≤ 8 that address "you" directly
- Vary line counts: some one-liners, some 4–6 short lines

## Banned words and phrases (zero uses)

liminal, luminous, ephemeral, gossamer, tapestry, symphony, whisper (any form),
soul, sacred, shimmer, iridescent, "the weight of", "something like",
"a kind of", unspoken, untold, "quiet hum", "gentle hum", threshold (as
metaphor), cathedral (as metaphor), alchemy, "in this moment", "the space
between", ache/aching, "the world" as a vague subject.

## Rationed words (max uses across your 60)

light/lights (6) · dark/darkness (4) · silence/silent (3) · breath/breathe (2)
· moon (2) · stars (2) · dream/dreams (3) · window/windows (5) · coffee (4,
except hours 05–09 may use 6) · clock/watch (2 — the reader has a clock;
don't narrate timekeeping) · sleep (4 in hours 22–04, otherwise 2)

## Voice

Plainspoken American English. Wit welcome. Sentiment must be earned by the
image, never announced. Concrete beats abstract every time: brand names, street
furniture, job titles, body parts, foods, tools. "A Honda idling outside the
ER" beats "a car in the night." The reader is one person, probably on a phone,
at exactly this minute — many poems can act like they know that, but don't
overdo direct address.

Your hour sits inside a 24-hour arc (notes below). Occasionally acknowledge who
is actually awake at your hour — night nurses, bakers, new parents, other
hemispheres at lunch — but don't make every poem a census of occupations.

## The 24-hour arc

- **00** The day's basement. Closers, gamers, new parents, the grief-shifted,
  other hemispheres at lunch. Last thoughts before shutdown, or the first of
  something free.
- **01** The hour of bad math: what time must I fall asleep to get six hours.
  Bar close approaching, kitchens hosing down, dorm hallways.
- **02** Insomnia's main office. The mind audits everything since 1994. Shift
  workers' lunch break. International flights mid-ocean.
- **03** The body's hour: hospitals, hospice, labor and delivery, bakers'
  alarms. Lowest body temperature of the night. Nothing is performed at 3 a.m.
- **04** Pre-verbal world. Fish markets, paper mills, first alarms of the
  longest commuters, farmers. The day exists but hasn't spoken yet.
- **05** The disciplined and the desperate: gym lights, prayer, AA chips,
  bread proofing, coffee makers on timers, first buses pulling out.
- **06** The machinery starts. School-day logistics, showers queueing, traffic
  voices on the radio.
- **07** Cereal hour. Lunchboxes, lost shoes, the front-door checklist,
  podcasts and dread.
- **08** The merge. On-ramps, drop-off lanes, elevator small talk, the inbox
  opening like a fridge.
- **09** Fluorescent hour. Standups, the first real meeting, the second
  coffee, the plan for the day still intact.
- **10** The one honest work hour. Deep focus or elaborate avoidance. The
  tradespeople are already four hours in.
- **11** Hunger negotiations. Is it too early for lunch. Errands, retirees at
  the bank, the morning's promises renegotiated.
- **12** Top of the arc. Sandwiches, break-room microwaves, sun as high as it
  gets, diners, the half-day feeling.
- **13** The full-stomach hour. Warehouse floors, riding mowers, meetings
  people fight sleep through, siestas elsewhere.
- **14** The long flat middle. School buses staging, IV bags changed, the
  afternoon's first regret.
- **15** School's out. Snacks, crossing guards, the workday slump, the day
  quietly deciding what it was.
- **16** The fray. Last meetings, early quitters, gyms filling.
- **17** The reverse merge. Traffic, daycare pickup at a run, the drink poured
  early, aprons going on.
- **18** Kitchen hour. Onions in pans, news on, kids called twice, the day's
  first honest conversation.
- **19** Tables. Dinner in progress or cleared, practice pickups, dishwashers
  starting.
- **20** The soft enclosure. Homework, TV glow, porches, bath time, the second
  wind or the first surrender.
- **21** Teenagers' hour. Texts, bars filling, laundry folded in front of
  shows, the day's unfinished list quietly forgiven.
- **22** Lights going out one by one. Night shifts arriving, doors locked, the
  couple's ten minutes of actual talk.
- **23** The ledger. Last words, last scrolls, tomorrow rehearsed, the day
  signed off with or without ceremony.

## Process and output

Draft more than 60; keep the best 60. Kill anything that sounds like every
other AI poem: if it could appear in any hour, it isn't finished; if it
congratulates itself on being tender, cut it.

Output: write ONE file, valid JSON, nothing else in it:

```json
{"hour": H, "poems": ["poem for :00", "poem for :01", "... exactly 60 strings"]}
```

Use `\n` inside strings for line breaks. Exactly 60 entries. Validate the JSON
parses and the count is 60 before finishing.

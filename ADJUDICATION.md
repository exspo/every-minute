# Repetition Adjudication — working record

The gate (`gate_v2.py`) models a reading session, not the whole book: a reader
who is awake at 8 p.m. is awake at 9 p.m., and nobody reads 00:18 and 23:41
together. Pairs close on the clock are held to a strict bar; distant pairs are
judged as mirrors or texture.

## Policy

- **Within ~3 hours (circular):** same joke or image twice = one gets rewritten.
  The stronger instance survives. Applied across three passes: 81 rewrites after
  DESTROYER round 1, 83 + 23 + 2 after DESTROYER round 2's redesign signal.
- **Beyond the session window:** shared phrases and images are kept when they
  work as day/night mirrors, arcs, or recurring cast, and killed when they are
  the same joke rediscovered. Every kept pair is pinned in `gate_v2.py`'s
  allowlist with a one-line reason; the gate re-flags anything new.
- **Form quotas** (BRIEF.md): the mechanical one — at least ten poems of eight
  words or fewer per hour — is now checked by the gate. All 24 hours pass.

## Deliberate recurring cast and motifs (not defects)

- The nurse who writes the time in the chart: 05:06, 09:06, 10:06, 14:02, 23:54
- The dog's day: 04:06 (outvoted), 07:03 (sunbeam), 21:13 (bedtime)
- Blue glow on ceilings, escalating: 00:48, 22:28, 23:39
- "You will not remember": 03:43, 09:38, 14:48 — the book's own thesis
- The avoided email: 05:16 → 11:25 → 14:42 → 16:40
- The plan's decay: 09:09 → 11:18 → 13:09 → 14:53
- The traveling grocery list ("the thing for the sink"): 01:48, 15:13
- Court in session: 02:00 (the insomnia court), reprised 10:25
- Same-minute twins: 02:30/14:30, 05:45/17:45
- Mirrors: oven light (00:25/18:39), moths (03:07/21:42), train doors
  (08:46/17:23), lost and found (00:42/08:44), grease pencils (03:58/17:57),
  the bulb over the range (05:09/22:12), nurses' meals (01:16/20:15/18:41)
- The working men and women: "a man in a…", "a woman in a…" vignettes across
  the day — the same crew seen at different hours
- Overheard through walls and floors (each a different line): 00:18, 04:31,
  05:20, 06:12, 06:41, 08:10, 23:41
- Receipts, three keeping their THANK YOU COME AGAIN: 03:11, 19:31 (+ variants
  at 04:15, 06:16, 10:33, 23:18 with distinct closers)

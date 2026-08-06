# Every Minute

1,440 poems, one for each minute of the day. The site shows only the poem for
the current minute, in the reader's time zone. No archive, no browsing.

- `BRIEF.md` — the master style brief that governed all 1,440 poems
- `hours/hour_HH.json` — 60 poems per hour, index = minute
- `template.html` — site shell; `__POEMS__` and `__WORDCOUNT__` injected at build
- `assemble.py` — validates, runs the QA report, builds `docs/index.html`
- `docs/` — published via GitHub Pages at everyminute.day

Written by Claude, August 2026.

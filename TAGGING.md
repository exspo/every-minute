# Image-tagging instructions

For each poem, emit 1-3 tags naming its CENTRAL image, object, scene, or joke.
Not every noun — only what the poem is *about*. A reader who saw two poems with
the same central image an hour apart would feel the repeat; tags exist to catch
that.

Rules:
- lowercase, ascii, hyphenate compounds: `trash-curb`, `practice-pickup`,
  `dryer-buzzer`, `motion-light`, `second-coffee`
- Use the plainest generic word: `trash` not garbage/refuse, `car` not sedan
  (but keep the specific noun when the specific thing IS the image: `minivan`
  only if minivan-ness matters, else `car`)
- First tag = the central object/scene. Second/third only if the poem has a
  second load-bearing image or a distinctive joke shape worth tracking
  (`definition-form`, `receipt-form`, `instruction-form`, `overheard`,
  `list-form` for found-forms)
- People: tag the role when central: `nurse`, `baker`, `teenager`, `new-father`,
  `grandmother`, `crossing-guard`, `night-shift`
- Abstract poems with no concrete image: tag the subject: `insomnia-math`,
  `regret`, `minute-itself`
Output file (valid JSON, nothing else):
{"hour": H, "tags": [["tag1","tag2"], ... exactly 60 entries, index = minute]}

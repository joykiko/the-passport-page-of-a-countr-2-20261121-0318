# Submission reasoning — the-passport-page-of-a-countr-2-20261121-0318
## "Republic of Talmar — Passport of Mara Ilsa Venn, Port Anselm"

- **Competition:** The Passport Page of a Country That Isn't There.
  Pot $50 (20 places, 1st $18), USDC on Solana. Deadline 2026-11-21
  06:18 UTC (13:18 WIB). Entry fee $0 (free-only rule: passed).
  Force Last — last submission before deadline is the final entry.
  Quota: max 10/day, 20 total (real account cap ±3 — max 2 probes + 1 final).
  Transcripts required (not strict-transcripts): standard upload bundle.
  Repo created after open (makefun anchor e804a69795ab57ddf2c794447dbfb4bc46ee101d,
  round 34144492).

### 1. Rubrik → Bukti (judge brief, in order)
- **(1) Is an invented passport spread** — bukti: the whole 1024×1024
  image is one open two-page spread, data page left, visa page right,
  nothing else in frame except the desk it lies on.
- **(2) Typography/layout that holds together** — bukti: one cream paper,
  one navy/gold palette, DejaVu Serif for the country name, DejaVu Sans
  for fields, DejaVu Sans Mono for the MRZ; fixed margins, one rule
  under each header, page numbers 2 and 3. Visual QA (read the render
  twice) found and fixed: portrait overflowing its frame, three label
  collisions (TYPE/CODE row, SEX/ISSUE/EXPIRY row), fee stamp covering
  the property line. Final render: zero overlaps, zero garbled text.
- **(3) Stamps, dates, issue details agree; plausible travel history** —
  bukti: issued 02 JUN 2026; Arvost visa valid 18 AUG–17 SEP 2026;
  Arvost in 18 AUG, out 02 SEP; Selkirk in 05 SEP, out 20 SEP — every
  stamp after issue, the Arvost stay inside visa validity. MRZ check
  digits computed by ICAO 9303 in code (doc, DOB, expiry, personal,
  composite) and verified by re-reading the rendered strip.
- **(4) Portrait and place-name belong together** — bukti: Mara Ilsa
  Venn, born 14 MAR 1987 in Port Anselm, dark bob, sea-light portrait,
  navy jacket — a harbour-town holder for a harbour republic whose arms
  are a lighthouse over three waves.
- **(5) One telling paperwork detail** — bukti: "CONDITION OF ENTRY —
  Art. 7, Aliens Act: Employment prohibited. Fishing in Talmar
  territorial waters requires a permit from the Harbour Office, Port
  Anselm." It says what Talmar is without a caption. Plus the human
  trace: handwritten "Mara — ring when you land. — E." and a dog-eared
  corner.

### 2. Angka terukur
- Local: 1024×1024 PNG, 159,362 bytes (limit 1,048,576); deterministic
  2× (md5 identical across runs); `main.py` runs in <1 s, no network.
- Live leaderboard at build time (21 Nov ~12:12 WIB, 1,182 entries,
  1,178 rated): rank 1 = 0.903418, rank 10 = 0.882310, rank 20 (last
  paid) = 0.871719, rank 80 (final-heat cut) = 0.845120, median = 0.691469.
- Gap to close: from a typical new entry near the median (0.69) to the
  rank-80 cut is ~0.15; to the last paid place ~0.18. The lever is the
  register itself (see §3) executed as a verifiable document, not a
  poster — the criteria are ordered, and criterion 3 (dates that agree)
  is where most entries fail first.
- Provisional rate: not yet known — parent submits; read it after submit.

### 3. Pembanding
- Leaders live (titles): "Republic of Kestrava — passport (causeway, low
  water only) v2" (0.9034), "Republic of Sarygol — Hydrologist's
  Biometric Passport Spread", "Republic of Altvarra: mountain guide's
  passport", "Republic of Isenmere — Passport of Katri Aho, Ice-Road
  Driver", "Republic of Skerrholm — Passport Spread of a Lighthouse
  Keeper". Mechanism shared by all of them: a named republic + ONE
  specific person/occupation tied to the place + one concrete geographic
  quirk. This entry uses exactly that mechanism (Talmar + harbour holder
  + fishing-permit waters), and adds what the titles do not show: a
  fully checkable date chain and a computed MRZ.
- Baseline it leaves behind: generic pretty passport posters with
  slogans or mismatched stamps — the judge's criterion 1 and 3 punish
  those first, and this entry is built to pass both before anything else.

### 4. Kelemahan jujur + mitigasi
- Biggest weakness: the portrait is a flat drawing, not a photograph —
  a real-looking data page would be stronger on criterion 4. Mitigation:
  the drawing is clean, front-facing, correctly framed and clipped;
  all text is code-rendered (zero garbled AI text, which is the more
  common failure in this heat).
- Risk that cannot be closed: the field is 1,182 entries and the top 80
  cut (0.845) sits far above the median (0.691); pairwise-judge variance
  across 12 games is real. Mitigation: this is probe 1 — read the
  provisional rate, iterate only if it shows a path near 0.845.
- No claim is made that this beats rank 1 (0.9034); the honest target
  for probe 1 is a rate at or above the rank-80 cut.

### 5. Keputusan jatah (Force Last sadar)
- Ini probe 1 dari maks 3 (2 probe + 1 final). Entries made: 0 (parent
  submits; this session does NOT run bundle/submit).
- Force Last: this probe becomes the standing final entry; a v2 only if
  the provisional rate shows a concrete, fixable gap (e.g. a criterion
  the judge's reason names) — not on a hunch.

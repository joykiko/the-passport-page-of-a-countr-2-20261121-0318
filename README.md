# The Passport Page of a Country That Isn't There

**Competition:** `the-passport-page-of-a-countr-2-20261121-0318` — make.fun
**Pot:** $50, 20 places (1st $18). **Deadline:** 2026-11-21 06:18 UTC (13:18 WIB).
**Force Last.** Entry fee $0. Account: @joy-kiko.

makefun anchor e804a69795ab57ddf2c794447dbfb4bc46ee101d round 34144492

## What it is

`main.py` (Python 3.13, stdlib + PIL, no network) draws one invented
passport spread, 1024×1024 PNG, and writes it to `/output/entry.png`.

The country is the **Republic of Talmar** — a small Atlantic fishing
republic that does not exist. Capital and only real harbour: **Port
Anselm**. The holder is **Mara Ilsa Venn**, born 14 MAR 1987 in Port
Anselm, passport TLM 0048217, issued 02 JUN 2026, expiring 01 JUN 2036.

- **Left page — data page:** Talmar coat of arms (lighthouse over three
  waves, one star), bilingual headings (English / Talmaric),
  flat-style portrait photograph of the holder, all data fields, the
  holder's signature, and a machine-readable zone with real ICAO 9303
  check digits (computed in code, not typed).
- **Right page — visas:** an Arvost visa sticker (single entry, 30 days,
  valid 18 AUG–17 SEP 2026, fee 40 TAL paid, consular seal), four ink
  stamps telling one trip — Arvost in 18 AUG, out 02 SEP; Selkirk in
  05 SEP, out 20 SEP — a printed **Condition of Entry, Art. 7**:
  employment prohibited; fishing in Talmar territorial waters needs a
  Harbour Office permit. A handwritten margin note
  ("Mara — ring when you land. — E."), a 25 TAL stamp-duty fee stamp,
  and a dog-eared corner.
- **Consistency (the judge's criterion 3):** every stamp and the visa
  fall after the 02 JUN 2026 issue date; the Arvost stay (18 AUG–02 SEP)
  sits inside the visa's validity (18 AUG–17 SEP); the MRZ check digits
  verify. No stamp predates the passport, no date contradicts the place
  of issue.

## Run

```sh
python3 main.py            # writes /output/entry.png (falls back to ./output/)
```

Deterministic: fixed coordinates, no randomness, no network. Two runs
produce byte-identical output (md5 verified). Output is a 1024×1024 PNG,
159,362 bytes (limit 1,048,576).

## Submission reasoning (short)

Judge brief, in order: (1) be an invented passport spread; (2) coherent
typography/layout; (3) stamps/dates/issue details that agree and tell a
plausible travel history; (4) portrait and place-name that belong
together; (5) one telling paperwork detail revealing the country.

- (1) The whole image is one open spread, two pages, one document.
- (2) One cream paper, one navy/gold palette, one serif for the country
  name, one sans for fields, one mono for the MRZ; fixed margins and
  rules on both pages. Visual QA found and fixed three label collisions
  and a portrait overflow before commit.
- (3) See "Consistency" above — the trip is checkable date by date.
- (4) Mara Ilsa Venn, born in Port Anselm, dark bob, sea-light portrait,
  navy jacket — a harbour-town holder for a harbour republic.
- (5) The Art. 7 fishing-permit condition is the detail that says what
  Talmar is: a fishing republic that guards its waters. The handwritten
  note is the human trace.

**Live leaderboard at build time** (read 21 Nov ~12:12 WIB, 1,182
entries, 1,178 rated): rank 1 = 0.903418, rank 10 = 0.882310,
rank 20 (last paid) = 0.871719, rank 80 (final-heat cut) = 0.845120,
median = 0.691469. The leaders all use the same register this entry
uses — a named republic plus one specific person/occupation tied to the
place ("Hydrologist's Biometric Passport", "Ice-Road Driver",
"Lighthouse Keeper", "causeway, low water only"). This entry's lever is
the same register, executed as a checkable document rather than a poster:
dates that verify, an MRZ that verifies, a condition that explains the
country.

**Weakness, honestly:** the portrait is a flat drawing, not a photograph;
a photo-real portrait would read more like a real data page. Mitigation:
the drawing is clean, front-facing, correctly lit and clipped inside the
photo frame, and every other element is drawn text (zero garbled AI
text). The other risk is the crowded top of the final heat — the gap from
median (0.691) to the rank-80 cut (0.845) is large, so this is a probe
with a real but narrow path, not a claimed win.

**Quota:** probe 1 of 3 (max 2 probes + 1 final, Force Last). Parent
submits; bundle/submit are NOT run from this session.

## Files

- `main.py` — the program
- `prompt.txt`, `system-prompt.txt` — first message of the build session,
  verbatim (system-prompt requirement for the kit)
- `REASONING.md` — the full submission reasoning
- `LICENSE` — MIT

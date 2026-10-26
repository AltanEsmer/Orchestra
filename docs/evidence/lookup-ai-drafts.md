# AI lookup drafts for the M3 shortfall

Drafted October 26, 2026. Altan asked: "Draft more AI lookup candidates in non-keyed request types, avoiding M1 named settings, for me to label." The [capacity screen](m3-capacity-screen.md) left lookup 11 to 24 rows short. These 30 drafts are proposals for that gap. None is accepted. Every one has a null human label and needs Altan's label and rationale, the blind AI check, and adjudication of flags under the brief's [drafting supplement](../collection-brief.md#ai-candidate-drafting-supplement-october-26-2026).

## What was drafted

The agent (Claude Opus 5.5 in Claude Code) wrote 30 queries, each naming its own invented organisation, so each is its own guide-v2 group. None is a keyed-record lookup, which has already reached its 40-row limit.

| Request type | Drafts |
| --- | ---: |
| Condition filter | 6 |
| Ordering or selection | 4 |
| Lookup, then aggregate | 4 |
| Category counts | 3 |
| Existence check | 3 |
| Distinct values | 2 |
| Compare entries in two sources | 2 |
| Free interval | 2 |
| Duplicate records | 2 |
| Lookup, then calculate | 2 |

If all 30 were accepted, lookup's second source would rise from 11 to 41 rows, against a need of 22 to 35. With BFCL's borderline rows, 11 of the 30 close the gap. Without them, 24 are needed. No request type would exceed its limit. These are projections, not results.

## Checks

`make_drafts.py` writes the bundle only if every check passes:

- **Names.** No capitalised name may match one in M1, the 40 earlier drafts, or the judged BFCL lookup candidates. Generic place words (Club, Centre, Library) and sentence-initial words do not count. A planted "Willow" was caught in a self-test.
- **Near-duplicates.** The highest Jaccard overlap with any M1 row, earlier draft, BFCL candidate, or other new draft is 0.29, under the brief's 0.5 threshold.
- **Cue words.** No draft uses "fictional", "table", "database", "calculate", "paragraph", or "handbook", the M1 cue words the brief lists. Source nouns vary: roster, register, inventory, ledger, log, archive, schedule, catalogue, calendar, timetable, and others.
- **Form.** There are 30 unique IDs and texts, one named setting each, with lengths from 9 to 24 words (median 18; M1's class medians run from 14 to 19).

The checks cannot establish that a label is correct or that a draft reads like a real user request.

## Boundaries to look at while labelling

These are agent observations for Altan's attention, not decisions:

- **N09** asks to sort titles from a stock list. In M1, sorting supplied words was direct answer. The difference here is that the records come from a named source.
- **N14, N29, and N30** look up records and then add, subtract, or take a percentage. Under the guide the first action is still lookup, but the arithmetic wording could suggest calculation.
- **N11** (unit 4) and **N26** (court 3) name one item by number but ask for an aggregate or a free slot, not one stored field. Decide whether they count as keyed-record lookups.
- **N23 and N24** compare two sources from the same organisation. Each is still one group.

## Provenance and exposure

The ignored bundle `data/raw/lookup-drafts-ai-2026-10-26/` holds the request, generation-context snapshots of the guide, brief and data protocol, `candidates.jsonl`, `query-only.jsonl`, `worksheet.md`, `check-report.json`, and `provenance.json`. The generator, `work/poteto/lookup-drafts/make_drafts.py` (SHA-256 `36846719…1084`), holds the draft text and checks M1's hash. `provenance.json` is `ac7c6f02…26a0`, and `candidates.jsonl` is `f0f22be4…a599`.

Generation parameters and the exact model revision are not exposed by this interface and are not invented here. Human edits at creation: none.

**Disclosure.** The drafting agent had read Altan's M2 validation-error hypotheses before drafting. The request types come from the capacity screen's type limits and the cue words from the brief's pre-M2 list, not from the errors. The exposure still has to be disclosed with any accepted row. The drafting agent also proposed each draft's label and type, so it cannot serve as the blind AI checker for them. The blind check must run separately on `query-only.jsonl`.

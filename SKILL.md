---
name: methods-provenance
description: Trace every parameter in a method section back to the run configuration, flag disagreements, list what has no source as not_reported, and produce a reproduction checklist. Use when asked to write, check or complete a Methods/Experimental section.
---

# Method sections that trace to a run

A method section is a set of numbers that should all exist somewhere in a config.
This skill matches them, quotes them, and says which ones have no source. It
never infers a value and it never rejects a case: a missing config produces a
table full of `not_reported`, which is a usable answer, not a failure.

## One command

**Where to run it.** The scripts resolve their own paths, so they work from
any working directory. If your shell starts in `/app/work` (the contract's work
directory), call the absolute path of the script —
`python3 /skills/weekly-skill/scripts/run.py --input /input/case.json --output /app/output`
— or `cd` into the folder holding this `SKILL.md` first and use the relative form
below.

```bash
python3 scripts/run.py --input /input/case.json --output /app/output
```

## What it writes

| file | content |
|---|---|
| `methods_checked.md` | the method text plus a parameter-provenance table and a checklist table |
| `provenance.json` | `parameters[]` and `checklist[]` |
| `result.json` | `provenance`, `checklist`, `coverage`, `not_reported`, `evidence` |

A provenance row is `{name, value, quote, char_start, char_end, source, source_value, status}`
with `status` ∈ `matched`, `conflict`, `not_reported`.

## Rules

1. **Match, do not infer.** `3e-4` and `0.0003` are the same number; `three times`
   and `repeats: 3` are the same value. Anything else is a `conflict`.
2. **No source, no value.** A parameter the config does not define is
   `not_reported` and appears under `uncertainty` with the quote that mentions it.
3. **Quotes are the evidence.** Every row carries the exact words from the text
   and a character range into `inputs/<name>`; `verify.py` re-slices them.
4. **Never reject.** Missing config, unreadable config, unknown parameter names —
   all produce a result with a stated reason.

## The checklist

Eight items: code version, dependencies, hardware, seeds, data split,
hyperparameters, runtime, evaluation metric. Each is `present` (found in the text
or the config) or `unknown`. Coverage below 5/8 lowers the score but keeps the
status meaningful.

## Failure handling

| situation | behaviour |
|---|---|
| text value disagrees with config | `conflict`, both values quoted, status `partial` |
| parameter not in config | `not_reported`, listed under `uncertainty` |
| no config file | every parameter `not_reported`, status `partial` |
| config not JSON | treated as absent, said so in `limits` |
| no method text | `cannot_determine` |

## Limits

- Only JSON configs are parsed; YAML/TOML are reported as absent rather than
  half-read.
- The parameter vocabulary is a fixed list; an unusual parameter name is not
  recognised and will not appear in the table.
- Numbers written in words are normalised for 3–5 only.

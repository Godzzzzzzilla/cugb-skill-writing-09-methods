# writing-09-methods

Parameter provenance and a reproduction checklist for Methods sections.
Submission for **写作09｜方法与实验章节写作** (product-arena-05).

## Design note — the zero-score trap

The obvious implementation hard-fails a case when the config is missing or a key
does not match. On hidden inputs that turns a small mismatch into a `rejected`
bundle and a zero. This skill never rejects: every unknown becomes
`not_reported`, the run continues, and the status becomes `partial` with the
reason. `selftest.py` includes a case with no config at all and asserts it still
produces a result.

## Measured on the bundled demo

| quantity | value |
|---|---|
| parameters found in the text | 10 |
| matched to the config | 10 |
| conflicts | 0 |
| `not_reported` | 0 |
| checklist items found | 6 / 8 |
| parameter quotes re-slicing | 10 / 10 |
| audit | 7/7, `status: success` |

## Files

```
SKILL.md               what an agent loads
scripts/run.py         provenance + checklist
scripts/verify.py      independent anchor verifier
scripts/selftest.py    15 checks, including a no-config case
scripts/armkit.py      shared core
examples/case.json     demo input (methods.md + config.json)
run/                   a real run
```

## Reproduce

```bash
python3 scripts/run.py --input examples/case.json --output /tmp/out
python3 scripts/verify.py --result /tmp/out/result.json
python3 scripts/selftest.py
```

## Failure handling

| input | behaviour |
|---|---|
| no config | all parameters `not_reported`, `partial`, no inference |
| value disagrees | `conflict`, both values quoted |
| unknown parameter name | not tabulated (fixed vocabulary) |
| no method text | `cannot_determine` |

# result.json

- `provenance[]` — `{name, value, quote, char_start, char_end, source, source_value, status, evidence_id}`.
- `checklist[]` — `{item, label, status, found_in[]}` for the eight reproduction items.
- `coverage` — `{parameters, matched, conflicts, not_reported, checklist_present, checklist_total}`.
- `not_reported[]` — parameter names with no source.
- `parameter_count`, `checklist_present`.

`status: success` requires no conflicts, no `not_reported` parameters, at least
five checklist items and every quote re-slicing. `partial` is a normal outcome
and always names its reason.

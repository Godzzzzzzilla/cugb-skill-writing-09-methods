# writing-09-methods — case demo-methods-01

- status: **success** (every parameter traces to the config and the checklist is covered)
- checks: 7/7 passed, ratio=1.0
- evidence: 10 anchored claims
- finished: 2026-11-25T07:54:51Z

## Result

```json
{
 "provenance": [
  {
   "name": "learning_rate",
   "value": "3e-4",
   "char_start": 78,
   "char_end": 99,
   "quote": "learning rate of 3e-4",
   "source": "inputs/methods.md",
   "source_value": 0.0003,
   "status": "matched",
   "evidence_id": "p1"
  },
  {
   "name": "batch_size",
   "value": "64",
   "char_start": 103,
   "char_end": 119,
   "quote": "batch size of 64",
   "source": "inputs/methods.md",
   "source_value": 64,
   "status": "matched",
   "evidence_id": "p2"
  },
  {
   "name": "epochs",
   "value": "12",
   "char_start": 125,
   "char_end": 134,
   "quote": "12 epochs",
   "source": "inputs/methods.md",
   "source_value": 12,
   "status": "matched",
   "evidence_id": "p3"
  },
  {
   "name": "optimizer",
   "value": "AdamW",
   "char_start": 67,
   "char_end": 72,
   "quote": "AdamW",
   "source": "inputs/methods.md",
   "source_value": "AdamW",
   "status": "matched",
   "evidence_id": "p4"
  },
  {
   "name": "schedule",
   "value": "cosine",
   "char_start": 142,
   "char_end": 156,
   "quote": "cosine schedul",
   "source": "inputs/methods.md",
   "source_value": "cosine",
   "status": "matched",
   "evidence_id": "p5"
  },
  {
   "name": "hardware",
   "value": "A100",
   "char_start": 245,
   "char_end": 269,
   "quote": "A100 40GB for approximat",
   "source": "inputs/methods.md",
   "source_value": "A100 40GB",
   "status": "matched",
   "evidence_id": "p6"
  },
  {
   "name": "beam_width",
   "value": "4",
   "char_start": 341,
   "char_end": 353,
   "quote": "beam width 4",
   "source": "inputs/methods.md",
   "source_value": 4,
   "status": "matched",
   "evidence_id": "p7"
  },
  {
   "name": "repeats",
   "value": "three",
   "char_start": 404,
   "char_end": 415,
   "quote": "three times",
   "source": "inputs/methods.md",
   "source_value": 3,
   "status": "matched",
   "evidence_id": "p8"
  },
  {
   "name": "dataset",
   "value": "standard split",
   "char_start": 321,
   "char_end": 335,
   "quote": "standard split",
   "source": "inputs/methods.md",
   "source_value": "standard split",
   "status": "matched",
   "evidence_id": "p9"
  },
  {
   "name": "wall_clock_hours",
   "value": "9",
   "char_start": 273,
   "char_end": 280,
   "quote": "9 hours",
   "source": "inputs/methods.md",
   "source_value": 9,
   "status": "matched",
   "evidence_id": "p10"
  }
 ],
 "checklist": [
  {
   "item": "code_version",
   "label": "the exact code revision",
   "status": "unknown",
   "found_in": []
  },
  {
   "item": "dependencies",
   "label": "pinned dependency versions",
   "status": "unknown",
   "found_in": []
  },
  {
   "item": "hardware",
   "label": "the hardware the numbers came from",
   "status": "present",
   "found_in": [
    "method text",
    "config"
   ]
  },
  {
   "item": "seeds",
   "label": "random seeds and repetition count",
   "status": "present",
   "found_in": [
    "method text",
    "config"
   ]
  },
  {
   "item": "data_split",
   "label": "which split was used",
   "status": "present",
   "found_in": [
    "method text",
    "config"
   ]
  },
  {
   "item": "hyperparameters",
   "label": "the hyperparameters",
   "status": "present",
   "found_in": [
    "method text",
    "config"
   ]
  },
  {
   "item": "runtime",
   "label": "how long a run takes",
   "status": "present",
   "found_in": [
    "method text",
    "config"
   ]
  },
  {
   "item": "evaluation_metric",
   "label": "the metric and its definition",
   "status": "present",
   "found_in": [
    "method text",
    "config"
   ]
  }
 ],
 "coverage": {
  "parameters": 10,
  "matched": 10,
  "conflicts": 0,
  "not_reported": 0,
  "checklist_present": 6,
  "checklist_total": 8
 },
 "not_reported": [],
 "parameter_count": 10,
 "checklist_present": 6
}
```

## Evidence

| id | claim | locator | ok |
|---|---|---|---|
| p1 | learning_rate = 3e-4 (matched) | `inputs/methods.md[78:99]` | ✓ |
| p2 | batch_size = 64 (matched) | `inputs/methods.md[103:119]` | ✓ |
| p3 | epochs = 12 (matched) | `inputs/methods.md[125:134]` | ✓ |
| p4 | optimizer = AdamW (matched) | `inputs/methods.md[67:72]` | ✓ |
| p5 | schedule = cosine (matched) | `inputs/methods.md[142:156]` | ✓ |
| p6 | hardware = A100 (matched) | `inputs/methods.md[245:269]` | ✓ |
| p7 | beam_width = 4 (matched) | `inputs/methods.md[341:353]` | ✓ |
| p8 | repeats = three (matched) | `inputs/methods.md[404:415]` | ✓ |
| p9 | dataset = standard split (matched) | `inputs/methods.md[321:335]` | ✓ |
| p10 | wall_clock_hours = 9 (matched) | `inputs/methods.md[273:280]` | ✓ |

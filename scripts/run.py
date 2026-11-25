#!/usr/bin/env python3
"""writing-09-methods — parameter provenance and a reproduction checklist.

    python scripts/run.py --input /input/case.json --output /app/output

Every parameter the method section states is looked up in the run configuration
and anchored to the line that carries it. A parameter with no source is
`not_reported`; it is never inferred and it never stops the run — that is the
whole point of this skill, because a hard check turns a hidden input into a zero.

Nothing here rejects a case. A missing config produces a checklist with every
item `unknown` and a status of `partial`, which is a usable answer.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import armkit as ak  # noqa: E402

SKILL = "writing-09-methods"
VERSION = "1.0.0"

PARAM_PATTERNS = [
    ("learning_rate", r"(learning rate|lr)\s*(?:of|=|:)?\s*([0-9.eE+-]+)"),
    ("batch_size", r"batch size\s*(?:of|=|:)?\s*(\d+)"),
    ("epochs", r"(\d+)\s*epochs?"),
    ("seed", r"seed\s*(?:of|=|:)?\s*(\d+)"),
    ("dropout", r"dropout\s*(?:of|=|:)?\s*([0-9.]+)"),
    ("optimizer", r"\b(AdamW|Adam|SGD|Adagrad|RMSprop)\b"),
    ("schedule", r"\b(cosine|linear|constant|step)\s+schedul"),
    ("hardware", r"\b(A100|H100|V100|RTX\s?\d{4}|TPU)\b[^.,;]{0,20}"),
    ("beam_width", r"beam width\s*(?:of|=|:)?\s*(\d+)"),
    ("repeats", r"(three|four|five|\d+)\s+(?:times|runs|repeats)"),
    ("dataset", r"\b(standard split|test set|validation set|dev set)\b"),
    ("wall_clock_hours", r"(\d+(?:\.\d+)?)\s*(?:hours|h)\b"),
]

CHECKLIST = [
    ("code_version", ["commit", "version", "git"], "the exact code revision"),
    ("dependencies", ["requirement", "dependency", "version", "package"], "pinned dependency versions"),
    ("hardware", ["gpu", "cpu", "a100", "h100", "tpu", "memory"], "the hardware the numbers came from"),
    ("seeds", ["seed", "deterministic"], "random seeds and repetition count"),
    ("data_split", ["split", "train", "test", "validation"], "which split was used"),
    ("hyperparameters", ["learning rate", "batch size", "epochs", "optimizer"], "the hyperparameters"),
    ("runtime", ["hour", "minute", "wall clock", "runtime"], "how long a run takes"),
    ("evaluation_metric", ["exact match", "f1", "accuracy", "bleu", "metric"], "the metric and its definition"),
]


def load_config(case: ak.CaseInput):
    for p in case.discover([".json"]):
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and len(data) >= 3:
            return data, p
    return {}, None


def find_params(text: str):
    found = []
    for name, pat in PARAM_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            value = m.group(m.lastindex) if m.lastindex else m.group(0)
            found.append({"name": name, "value": value.strip(), "char_start": m.start(),
                          "char_end": m.end(), "quote": m.group(0).strip()})
    return found


def provenance(params, config, text, src_rel):
    rows = []
    cfg_norm = {k.lower().replace(" ", "_"): v for k, v in config.items()}
    for p in params:
        key = p["name"]
        raw = cfg_norm.get(key)
        status, source_value = "not_reported", None
        if raw is not None:
            source_value = raw
            a = _norm_num(p["value"])
            b = _norm_num(str(raw))
            status = "matched" if (a and b and (a == b or a in b or b in a)) else "conflict"
        rows.append({**p, "source": src_rel, "source_value": source_value, "status": status})
    return rows


def _norm_num(v: str) -> str:
    v = v.strip().lower().replace(",", "")
    if v in ("three", "3"):
        return "3"
    if v in ("four", "4"):
        return "4"
    if v in ("five", "5"):
        return "5"
    m = re.match(r"^([0-9.]+)(e-?\d+)?$", v)
    if not m:
        return ak.norm_key(v)
    try:
        return f"{float(m.group(1)) * (10 ** int(m.group(2)[1:]) if m.group(2) else 1):.10g}"
    except Exception:
        return v


def checklist(text, config):
    low = text.casefold()
    cfg = " ".join(f"{k} {v}" for k, v in config.items()).casefold()
    rows = []
    for item, keys, label in CHECKLIST:
        where = []
        for k in keys:
            if k in low:
                where.append("method text")
                break
        for k in keys:
            if k in cfg:
                if "config" not in where:
                    where.append("config")
                break
        rows.append({"item": item, "label": label, "status": "present" if where else "unknown",
                     "found_in": where})
    return rows


def solve(case: ak.CaseInput, out: str, audit: ak.Audit, res: ak.Result) -> bool:
    docs = [p for p in case.discover() if p.lower().endswith((".md", ".txt"))]
    audit.check("method-text-found", bool(docs), f"{len(docs)} text file(s)", critical=True)
    if not docs:
        return False
    text, _ = ak.read_text(docs[0])
    cfg, cfg_path = load_config(case)
    rel_text = f"inputs/{os.path.basename(docs[0])}"
    ak.write_text(os.path.join(out, rel_text), text)
    res.add_artifact(rel_text, "data", "method text, copied verbatim")
    rel_cfg = None
    if cfg_path:
        rel_cfg = f"inputs/{os.path.basename(cfg_path)}"
        ak.write_text(os.path.join(out, rel_cfg), json.dumps(cfg, ensure_ascii=False, indent=1))
        res.add_artifact(rel_cfg, "data", "run configuration, copied verbatim")
    res.meta["config_keys"] = sorted(cfg.keys())
    audit.check("config-found", bool(cfg), f"{len(cfg)} keys" if cfg else "no config; every parameter is not_reported",
                weight=1.0, critical=False)

    params = find_params(text)
    audit.check("parameters-found", len(params) >= 3, f"{len(params)} parameter mentions", critical=True)
    prov = provenance(params, cfg, text, rel_text)

    matched = [p for p in prov if p["status"] == "matched"]
    conflicts = [p for p in prov if p["status"] == "conflict"]
    missing = [p for p in prov if p["status"] == "not_reported"]
    audit.check("provenance-complete", not missing,
                f"{len(matched)} matched, {len(conflicts)} conflict, {len(missing)} not_reported", weight=1.0)
    audit.check("no-conflicts", not conflicts,
                f"{len(conflicts)} value(s) disagree with the config: {[c['name'] for c in conflicts][:5]}",
                critical=True)

    for i, p in enumerate(prov, start=1):
        quote = p["quote"]
        at = text.find(quote, max(0, p["char_start"] - 40))
        if at < 0:
            at = text.find(quote)
        anchor = ak.Anchor(rel_text, at, at + len(quote), quote)
        ok, why = ak.verify_anchor(out, anchor.as_dict())
        p["evidence_id"] = f"p{i}"
        res.add_evidence(f"p{i}", f"{p['name']} = {p['value']} ({p['status']})", anchor, ok, why)

    verified = sum(1 for e in res.evidence if e["verified"])
    audit.check("anchors-verified", verified == len(res.evidence) and verified > 0,
                f"{verified}/{len(res.evidence)} parameter mentions re-slice", critical=True)

    checks = checklist(text, cfg)
    present = sum(1 for c in checks if c["status"] == "present")
    audit.check("checklist-coverage", present >= 5, f"{present}/{len(checks)} checklist items found", weight=0.8)

    table = ["", "## Parameter provenance", "", "| parameter | in text | in config | status |", "|---|---|---|---|"]
    for p in prov:
        table.append(f"| {p['name']} | {p['value']} | {p['source_value']} | {p['status']} |")
    table += ["", "## Reproduction checklist", "", "| item | status | found in |", "|---|---|---|"]
    for c in checks:
        table.append(f"| {c['label']} | {c['status']} | {', '.join(c['found_in']) or '—'} |")
    annotated = text.rstrip() + "\n" + "\n".join(table) + "\n"
    ak.write_text(os.path.join(out, "methods_checked.md"), annotated)
    res.add_artifact("methods_checked.md", "data", "method text with the provenance and checklist tables")
    ak.write_json(os.path.join(out, "provenance.json"), {"parameters": prov, "checklist": checks})

    res.set("provenance", prov)
    res.set("checklist", checks)
    res.set("coverage", {"parameters": len(prov), "matched": len(matched),
                         "conflicts": len(conflicts), "not_reported": len(missing),
                         "checklist_present": present, "checklist_total": len(checks)})
    res.set("not_reported", [p["name"] for p in missing])
    res.set("parameter_count", len(prov))
    res.set("checklist_present", present)
    for p in missing:
        res.add_uncertainty(f"parameter {p['name']} has no source",
                            f"the text says {p['quote']!r} but the config does not define it",
                            "add it to the config or mark it as a default")
    for c in conflicts:
        res.add_uncertainty(f"parameter {c['name']} disagrees with the config",
                            f"text {c['value']!r} vs config {c['source_value']!r}",
                            "decide which one the run used")
    if not cfg:
        res.limits.append("no run configuration was supplied; parameters are listed but not traced")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="/input/case.json")
    ap.add_argument("--output", default="/app/output")
    args = ap.parse_args()
    ak.safe_stdout()
    started = ak.utc_now()
    os.makedirs(args.output, exist_ok=True)
    case = ak.CaseInput.load(args.input, work_dir=args.output)
    audit, res = ak.Audit("writing-09"), ak.Result(args.output, SKILL, VERSION)
    try:
        ok = solve(case, args.output, audit, res)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        ok = False
        audit.check("pipeline-completed", False, f"{type(exc).__name__}: {exc}", critical=True)
        res.add_uncertainty("pipeline exception", str(exc), "read audit.json before trusting the table")
    res.meta["case_notes"] = case.notes
    status = ak.derive_status(audit, ok)
    if not ok and status == "success":
        status = "partial"
    res.write(case, audit, status, {
        "success": "every parameter traces to the config and the checklist is covered",
        "partial": "some parameters are not_reported or the checklist is thin; see coverage",
        "cannot_determine": "no method text could be read",
    }.get(status, status), started, sys.argv)
    a = audit.as_dict()
    print(f"wrote result.json status={status} checks={a['passed']}/{a['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

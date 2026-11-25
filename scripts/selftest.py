#!/usr/bin/env python3
"""Self-test for writing-09-methods."""
from __future__ import annotations
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import armkit as ak
import run as skill
PASS = FAIL = 0
def check(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print(f"  ok {n}" + (f" — {d}" if d else ""))
    else: FAIL += 1; print(f"  FAIL {n}" + (f" — {d}" if d else ""))
def main():
    print("writing-09 selftest")
    check("armkit pinned", bool(ak.VERSION), ak.VERSION)
    text = "We train with a learning rate of 3e-4 and batch size of 64 for 12 epochs."
    params = skill.find_params(text)
    names = {p["name"] for p in params}
    check("finds lr", "learning_rate" in names, ",".join(sorted(names)))
    check("finds batch", "batch_size" in names)
    check("finds epochs", "epochs" in names)
    prov = skill.provenance(params, {"learning_rate": 0.0003, "batch_size": 64, "epochs": 12}, text, "x")
    check("lr matches 3e-4 vs 0.0003", all(p["status"] == "matched" for p in prov if p["name"] == "learning_rate"))
    prov2 = skill.provenance(params, {"batch_size": 32}, text, "x")
    check("missing key is not_reported", any(p["status"] == "not_reported" for p in prov2))
    with tempfile.TemporaryDirectory() as td:
        case = ak.CaseInput.load(os.path.join(ROOT, "examples", "case.json"))
        audit, res = ak.Audit("t"), ak.Result(td, "writing-09")
        ok = skill.solve(case, td, audit, res)
        doc = res.write(case, audit, ak.derive_status(audit, ok), "t", ak.utc_now(), ["selftest"])
        check("demo completes", ok)
        check("status success", doc["status"] == "success", doc["status"])
        check("all parameters traced", doc["result"]["coverage"]["matched"] == doc["result"]["coverage"]["parameters"])
        check("checklist produced", len(doc["result"]["checklist"]) == 8)
        check("annotated text written", os.path.isfile(os.path.join(td, "methods_checked.md")))
        bad = [e for e in doc["evidence"] if not ak.verify_anchor(td, e["anchor"])[0]]
        check("anchors re-slice", not bad, f"{len(doc['evidence'])} anchors")
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "in"), exist_ok=True)
        open(os.path.join(td, "in", "m.md"), "w", encoding="utf-8").write("Learning rate of 1e-3 for 5 epochs.")
        json.dump({"id": "noconfig"}, open(os.path.join(td, "in", "case.json"), "w", encoding="utf-8"))
        case = ak.CaseInput.load(os.path.join(td, "in", "case.json"))
        audit, res = ak.Audit("t2"), ak.Result(os.path.join(td, "o"), "writing-09")
        ok = skill.solve(case, os.path.join(td, "o"), audit, res)
        check("no config does not reject", ok and res.payload["coverage"]["not_reported"] >= 1,
              str(res.payload["coverage"]))
    print(f"\n{PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1
if __name__ == "__main__":
    raise SystemExit(main())

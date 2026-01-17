import json
import copy
import subprocess
import sys

def run():
    completed = subprocess.run(
        [sys.executable, "run.py"],
        capture_output=True,
        text=True
    )
    return completed.stdout.strip(), completed.stderr.strip()

def test_determinism_repeat():
    out1, _ = run()
    out2, _ = run()
    assert out1 == out2, "Output is not deterministic"

def test_missing_field():
    code = """
from core.pipeline import run_pipeline
from core.refusal import Refusal
import json

query = {
  "pregnancy_weeks": 20,
  "medical_practitioner_involved": True
}

def load(p):
    with open(p) as f: return json.load(f)

try:
    run_pipeline(
        query,
        load("queries/query_schema.json"),
        load("rules/rules.json"),
        load("verdict/verdict_engine.json"),
        load("explanation/explanation_template.json")
    )
    print("FAIL")
except Refusal as r:
    print("PASS")
"""
    out = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True
    ).stdout.strip()
    assert out == "PASS", "Missing field did not refuse"

def test_unknown_field():
    code = """
from core.pipeline import run_pipeline
from core.refusal import Refusal
import json

query = {
  "pregnancy_weeks": 20,
  "medical_practitioner_involved": True,
  "emergency_context": False,
  "extra": 123
}

def load(p):
    with open(p) as f: return json.load(f)

try:
    run_pipeline(
        query,
        load("queries/query_schema.json"),
        load("rules/rules.json"),
        load("verdict/verdict_engine.json"),
        load("explanation/explanation_template.json")
    )
    print("FAIL")
except Refusal:
    print("PASS")
"""
    out = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True
    ).stdout.strip()
    assert out == "PASS", "Unknown field did not refuse"

def test_empty_symbols():
    code = """
from core.pipeline import run_pipeline
import json

query = {
  "pregnancy_weeks": 1,
  "medical_practitioner_involved": False,
  "emergency_context": False
}

def load(p):
    with open(p) as f: return json.load(f)

result = run_pipeline(
    query,
    load("queries/query_schema.json"),
    load("rules/rules.json"),
    load("verdict/verdict_engine.json"),
    load("explanation/explanation_template.json")
)

print(result["verdict"])
"""
    out = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True
    ).stdout.strip()
    assert out == "NOT_PROVABLE", "Empty symbols should be NOT_PROVABLE"

def test_forbidden_words():
    out, _ = run()
    forbidden = [
        "legal", "illegal", "allowed", "permitted",
        "valid", "compliant", "should", "can", "cannot"
    ]
    lowered = out.lower()
    for w in forbidden:
        assert w not in lowered, f"Forbidden word detected: {w}"

if __name__ == "__main__":
    test_determinism_repeat()
    test_missing_field()
    test_unknown_field()
    test_empty_symbols()
    test_forbidden_words()
    print("ALL TESTS PASSED")

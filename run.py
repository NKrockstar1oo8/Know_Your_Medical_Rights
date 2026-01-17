import json
from core.pipeline import run_pipeline
from core.refusal import Refusal
from core.logger import log_event

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    try:
        query = {
            "pregnancy_weeks": 20,
            "medical_practitioner_involved": True,
            "emergency_context": False
        }

        query_schema = load_json("queries/query_schema.json")
        ruleset = load_json("rules/rules.json")
        verdict_engine = load_json("verdict/verdict_engine.json")
        explanation_template = load_json(
            "explanation/explanation_template.json"
        )

        result = run_pipeline(
            query,
            query_schema,
            ruleset,
            verdict_engine,
            explanation_template
        )

        print(json.dumps(result, indent=2))

    except Refusal as r:
        log_event("REFUSAL", {"reason": r.reason})
        print(f"REFUSED: {r.reason}")

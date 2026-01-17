class SafetyGate:
    def __init__(self, policy):
        self.policy = policy

    def assert_no_llm_reasoning(self, context):
        if context.get("llm_used_for") not in (None, "explanation"):
            raise SafetyViolation("LLM used outside explanation sandbox")

    def assert_no_legal_inference(self, flags):
        if flags.get("inferred_legality", False):
            raise SafetyViolation("Legal inference detected")

    def assert_all_facts_explicit(self, facts):
        if any(fact is None for fact in facts):
            raise SafetyViolation("Missing legal facts")

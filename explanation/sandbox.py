def explain(verdict, proof_bundle):
    if verdict.status != "PROVABLE":
        raise ExplanationRefusal("Explanation not allowed")

    safety_gate.assert_no_legal_inference(...)
    safety_gate.assert_no_llm_reasoning(...)

    prompt = build_prompt(...)
    output = call_llm(prompt)

    validate_output(output)
    return output

def build_prompt(expl_input: ExplanationInput) -> str:
    return f"""
You are explaining a mechanically proven legal result.

CONCLUSION SYMBOL:
{expl_input.conclusion_symbol}

PROOF STEPS:
{expl_input.proof_steps}

STRICT RULES:
- Do NOT infer legality, rights, or permissions
- Do NOT add conditions
- Do NOT use words like legal, illegal, allowed, permitted
- Explain only what was checked and found true
"""

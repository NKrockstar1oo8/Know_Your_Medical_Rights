# ui_chat.py

import streamlit as st

from core.fact_extractor import FactExtractor
from core.rights_evaluator import RightsEvaluator
from core.sheets_logger import log_to_google_sheets

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Medical-Legal Rights Assistant",
    layout="wide",
)

# -------------------------------------------------
# Title & Description
# -------------------------------------------------
st.title("⚖️ Medical-Legal Rights Assistant")

st.markdown("""
Ask your question freely.

The system determines **only provable medical-legal rights** based on official Indian government documents:

• **NHRC – Charter of Patients’ Rights (2019)**  
• **IMC – Ethics Regulations (2002)**  

❗ **No guessing. No hallucination.**
""")

st.warning(
    "⚠️ This system logs anonymized inputs for academic evaluation. "
    "Do not include personal identifiers (names, phone numbers, addresses)."
)

# -------------------------------------------------
# Input box
# -------------------------------------------------
user_input = st.text_area(
    "Describe your issue:",
    height=120,
    placeholder="Describe what happened in the hospital or with the doctor…",
)

analyze_clicked = st.button("🔍 Analyze")

# -------------------------------------------------
# Processing pipeline
# -------------------------------------------------
if analyze_clicked and user_input.strip():

    extractor = FactExtractor()
    evaluator = RightsEvaluator()

    # ----------------------------
    # 1. Extract facts
    # ----------------------------
    facts = extractor.extract(user_input)

    # ----------------------------
    # 2. Evaluate rights
    # ----------------------------
    verdict = evaluator.evaluate(facts)

    # ----------------------------
    # 4. Log to Google Sheets (NEW)
    # ----------------------------
    try:
        log_to_google_sheets(
            user_input=user_input,
            extracted_facts=facts,
            verdict=verdict
        )
    except Exception:
        # Do NOT show to users (silent fail in production)
        import traceback
        traceback.print_exc()

    # -------------------------------------------------
    # Output — USER SAFE VIEW ONLY
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("⚖️ System Verdict")

    verdict_type = verdict.get("verdict_type")

    # ============================
    # PROVABLE
    # ============================
    if verdict_type == "PROVABLE":

        st.success("✅ Primary Proven Violation(s)")

        for v in verdict.get("primary_violations", []):
            st.markdown(f"### {v['id']}")
            st.markdown(f"**Source:** {v['source']}")
            st.markdown(f"📚 **Citation:** {v['citation']}")
            st.markdown("**What this means:**")
            for line in v.get("explanation", []):
                st.markdown(f"- {line}")

    # ============================
    # PROCEDURAL
    # ============================
    elif verdict_type == "PROCEDURAL":

        st.info("⚙️ Procedural Remedies Available")

        for r in verdict.get("procedural_remedies", []):
            st.markdown(f"### {r['id']}")
            st.markdown(f"**Source:** {r['source']}")
            st.markdown(f"📚 **Citation:** {r['citation']}")
            st.markdown("ℹ️ **What you can do:**")
            for line in r.get("guidance", []):
                st.markdown(f"- {line}")

    # ============================
    # NOT PROVABLE
    # ============================
    else:
        st.warning("❓ No legally provable determination")
        st.markdown("""
No legally decidable right or duty applies.

**What you can do**
- Provide more specific facts
- Clarify who acted (doctor / hospital)
- Mention emergency, refusal, or denial

The system will never guess — it answers only when proof is possible.
""")

    st.caption("📝 This interaction has been securely logged for audit and evaluation.")


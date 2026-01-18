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
    # 1. Extract facts (INTERNAL)
    # ----------------------------
    facts = extractor.extract(user_input)

    # ----------------------------
    # 2. Evaluate rights
    # ----------------------------
    verdict = evaluator.evaluate(facts)

    # ----------------------------
    # 3. Logging (silent)
    # ----------------------------
    try:
        log_to_google_sheets(
            user_input=user_input,
            extracted_facts=facts,
            verdict=verdict
        )
    except Exception:
        import traceback
        traceback.print_exc()

    # -------------------------------------------------
    # USER SAFE OUTPUT
    # -------------------------------------------------
    st.markdown("---")
    st.subheader("⚖️ System Verdict")

    verdict_type = verdict.get("verdict_type")

    provable_rights = verdict.get("primary_violations", [])
    procedural_rights = verdict.get("procedural_remedies", [])

    # ============================
    # PROVABLE
    # ============================
    if verdict_type == "PROVABLE":

        violated_ids = [r["id"] for r in provable_rights]

        st.success(
            "✅ **Proven Patient Right Violation(s):**\n\n" +
            "\n".join([f"• {rid}" for rid in violated_ids])
        )

        for right in provable_rights:
            st.markdown("---")
            st.markdown(f"### {right['id']}")
            st.caption(f"Source: {right['source']} — {right['citation']}")
            st.markdown("**What this right guarantees:**")
            for line in right.get("explanation", []):
                st.markdown(f"- {line}")

    # ============================
    # PROCEDURAL
    # ============================
    elif verdict_type == "PROCEDURAL":

        procedural_ids = [r["id"] for r in procedural_rights]

        st.warning(
            "⚠️ **Procedural Rights Implicated:**\n\n" +
            "\n".join([f"• {rid}" for rid in procedural_ids])
        )

        for right in procedural_rights:
            st.markdown("---")
            st.markdown(f"### {right['id']}")
            st.caption(f"Source: {right['source']} — {right['citation']}")
            st.markdown("**What this means:**")
            for line in right.get("explanation", []):
                st.markdown(f"- {line}")

        st.info(
            "ℹ️ **Scope Limitation**\n\n"
            "This system can identify applicable patient rights based on official documents. "
            "It cannot advise on what actions to take or how to proceed."
        )

    # ============================
    # NOT PROVABLE
    # ============================
    else:
        st.error(
            "❌ **No Patient Right Violation Could Be Proven**\n\n"
            "Based on the information provided, no legally provable patient right "
            "could be determined under the applicable documents."
        )

        st.markdown("""
**Why this may happen**
- Key facts are missing or unclear
- Emergency, refusal, or denial not explicitly stated
- Responsibility (doctor vs hospital) not specified

The system will never guess or assume.
""")

    st.caption("📝 This interaction has been securely logged for audit and academic evaluation.")

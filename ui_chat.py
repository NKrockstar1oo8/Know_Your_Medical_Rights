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
# Styling for proven rights (academic clean)
# -------------------------------------------------
st.markdown("""
<style>
.proven-right {
    border-left: 6px solid #2ecc71;
    background-color: rgba(46, 204, 113, 0.08);
    padding: 16px;
    margin: 20px 0;
    border-radius: 6px;
}
.proven-right h3 {
    color: #2ecc71;
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Title & Description
# -------------------------------------------------
st.title("⚖️ Medical-Legal Rights Assistant")

st.markdown("""
Ask your question freely.

The system determines **only provable medical-legal rights and duties**
based strictly on official Indian government documents:

• **NHRC – Charter of Patients’ Rights (2019)**  
• **IMC – Ethics Regulations (2002)**  

❗ **No guessing. No legal advice. No hallucination.**
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
    # 2. Evaluate rights & duties
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
    imc_duties = verdict.get("imc_duties", [])
    procedural_items = verdict.get("procedural_remedies", [])

    # ============================
    # PROVABLE RIGHTS
    # ============================
    if verdict_type == "PROVABLE":

        violated_ids = [r["id"] for r in provable_rights]
        
        for right in provable_rights:
            explanation_html = "".join(
                [f"<li>{line}</li>" for line in right.get("explanation", [])]
            )

            st.markdown(f"""
            <div class="proven-right">
                <h3>{right['id']}</h3>
                <p><b>Source:</b> {right['source']} — {right['citation']}</p>
                <p><b>What this right guarantees:</b></p>
                <ul>
                    {explanation_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # ----------------------------
        # IMC DUTIES (PARALLEL DISPLAY)
        # ----------------------------
        if imc_duties:
            st.markdown("---")
            st.subheader("🩺 Relevant Doctor Duties (IMC)")

            for duty in imc_duties:
                st.markdown(f"### {duty['id']}")
                st.caption(f"Source: {duty['source']} — {duty['citation']}")
                st.markdown("**What this duty requires:**")
                for line in duty.get("explanation", []):
                    st.markdown(f"- {line}")

    # ============================
    # PROCEDURAL ONLY
    # ============================
    elif verdict_type in ("PROCEDURAL", "PROCEDURAL_REMEDY_AVAILABLE"):

        procedural_ids = [p["id"] for p in procedural_items]

        st.warning(
            "⚠️ **Procedural / Ethical Concerns Identified:**\n\n" +
            "\n".join([f"• {pid}" for pid in procedural_ids])
        )

        for item in procedural_items:
            st.markdown("---")
            st.markdown(f"### {item['id']}")
            st.caption(f"Source: {item['source']} — {item['citation']}")
            st.markdown("**What this means:**")
            for line in item.get("explanation", []):
                st.markdown(f"- {line}")

        st.info(
            "ℹ️ **Scope Limitation**\n\n"
            "This system identifies applicable rights and professional duties "
            "based strictly on official documents. "
            "It does not advise on actions or remedies."
        )

    # ============================
    # NOT PROVABLE
    # ============================
    else:
        st.error(
            "❌ **No Patient Right or Duty Could Be Proven**\n\n"
            "Based on the information provided, no legally provable determination "
            "could be made under the applicable documents."
        )

        st.markdown("""
**Why this may happen**
- Key facts are missing or unclear  
- Emergency, refusal, or denial not explicitly stated  
- Responsibility (doctor vs hospital) not specified  

The system will never guess or assume.
""")

    st.caption("📝 This interaction has been securely logged for audit and academic evaluation.")

import os
import streamlit as st

from core.fact_extractor import FactExtractor
from core.rights_evaluator import RightsEvaluator
from core.chat_history import save_chat

# =====================================================
# APPLICATION MODE
# =====================================================
# DEVELOPMENT  -> local use (developer controls visible)
# PRODUCTION   -> public deployment (controls hidden)
# =====================================================

APP_MODE = os.getenv("APP_MODE", "DEVELOPMENT")

# =====================================================
# System setup
# =====================================================
fact_extractor = FactExtractor()
rights_evaluator = RightsEvaluator()

st.set_page_config(
    page_title="Medical-Legal Rights Assistant",
    page_icon="⚖️",
    layout="centered"
)

# =====================================================
# Sidebar — Developer Controls (DEV ONLY)
# =====================================================
if APP_MODE == "DEVELOPMENT":
    with st.sidebar:
        st.header("⚙️ System Controls")

        developer_mode = st.checkbox(
            "Developer Mode (show extracted facts)",
            value=True
        )

        st.caption(
            "Developer mode reveals internal diagnostic data. "
            "This panel is hidden in public deployment."
        )
else:
    developer_mode = False

# =====================================================
# UI Header
# =====================================================
st.title("⚖️ Medical-Legal Rights Assistant")

st.markdown(
    """
Ask your question **freely**.

The system determines **only provable medical-legal rights**
based on official Indian government documents:

• **NHRC – Charter of Patients’ Rights (2019)**  
• **IMC – Ethics Regulations (2002)**  

❗ **No guessing. No hallucination.**
"""
)

st.info(
    "⚠️ This system logs anonymized inputs for academic evaluation. "
    "Do not include personal identifiers (names, phone numbers, addresses)."
)

# =====================================================
# User Input
# =====================================================
user_input = st.text_area(
    "Describe your issue:",
    height=120
)

submit = st.button("🔍 Analyze")

# =====================================================
# On Submit
# =====================================================
if submit:
    if not user_input.strip():
        st.warning("Please describe your issue.")
    else:
        # -----------------------------
        # Fact Extraction
        # -----------------------------
        facts = fact_extractor.extract(user_input)

        # -----------------------------
        # Rights Evaluation
        # -----------------------------
        verdict = rights_evaluator.evaluate(facts)

        # -----------------------------
        # Audit Logging (ALWAYS)
        # -----------------------------
        save_chat(
            user_input=user_input,
            facts=facts,
            verdict=verdict
        )

        # =====================================================
        # Developer View (HIDDEN IN PRODUCTION)
        # =====================================================
        if developer_mode:
            st.subheader("🔍 Extracted Facts (Developer View)")
            st.json(facts)

        # =====================================================
        # User-Facing Verdict
        # =====================================================
        st.subheader("⚖️ System Verdict")

        # -------------------------
        # PROVABLE
        # -------------------------
        if verdict["verdict_type"] == "PROVABLE":

            primary_list = verdict.get("primary_violations", [])
            procedural = verdict.get("procedural_remedies", [])

            # Primary violation
            if primary_list:
                primary = primary_list[0]

                st.success(f"✅ Primary Proven Violation: **{primary['id']}**")
                st.markdown(f"**Source:** {primary['source']}")
                st.markdown(f"📚 **Citation:** {primary['citation']}")

                st.markdown("### ✅ What this means")
                for line in primary.get("explanation", []):
                    st.markdown(f"- {line}")

            # Additional violations
            if len(primary_list) > 1:
                st.markdown("---")
                st.subheader("➕ Other Proven Violations")

                for v in primary_list[1:]:
                    st.success(f"✅ Proven Violation: **{v['id']}**")
                    st.markdown(f"**Source:** {v['source']}")
                    st.markdown(f"📚 **Citation:** {v['citation']}")

                    for line in v.get("explanation", []):
                        st.markdown(f"- {line}")

            # Procedural remedies
            if procedural:
                st.markdown("---")
                st.subheader("⚙️ Procedural Remedies Available")

                for pr in procedural:
                    st.warning(f"⚖️ {pr['id']}")
                    st.markdown(f"**Source:** {pr['source']}")
                    st.markdown(f"📚 **Citation:** {pr['citation']}")

                    st.markdown("### ℹ️ What you can do")
                    for line in pr.get("explanation", []):
                        st.markdown(f"- {line}")

        # -------------------------
        # PROCEDURAL ONLY
        # -------------------------
        elif verdict["verdict_type"] == "PROCEDURAL_REMEDY_AVAILABLE":
            st.warning("⚙️ Procedural Remedy Available")

            for pr in verdict.get("procedural_remedies", []):
                st.markdown(f"**{pr['id']}**")
                st.markdown(f"**Source:** {pr['source']}")
                st.markdown(f"📚 **Citation:** {pr['citation']}")
                for line in pr.get("explanation", []):
                    st.markdown(f"- {line}")

        # -------------------------
        # NOT PROVABLE
        # -------------------------
        else:
            st.info("❓ No legally provable determination")

            for reason in verdict.get("reasons", []):
                st.markdown(f"- {reason}")

            st.markdown(
                """
### ℹ️ What you can do
- Provide **more specific facts**
- Clarify **who acted** (doctor / hospital)
- Mention **emergency, refusal, or denial**

The system will never guess — it answers only when proof is possible.
"""
            )

        st.caption("📝 This interaction has been securely logged for audit and evaluation.")

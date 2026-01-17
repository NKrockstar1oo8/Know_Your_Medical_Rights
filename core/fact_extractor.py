# core/fact_extractor.py

import re


class FactExtractor:
    """
    Deterministic fact extractor.
    Extracts CLAIMS and OBSERVABLE FACTS only.
    No guessing. No legal reasoning. No ML.
    """

    def extract(self, text: str) -> dict:
        text = text.lower()

        facts = {
            # -----------------------------
            # Emergency related
            # -----------------------------
            "emergency_case": "unknown",
            "emergency_claimed": "no",
            "admission_denied": "unknown",
            "payment_demanded": "no",
            "treatment_refused": "no",

            # -----------------------------
            # Actors
            # -----------------------------
            "doctor_involved": "unknown",
            "hospital_involved": "unknown",

            # -----------------------------
            # Rights-related facts
            # -----------------------------
            "consent_issue": "unknown",
            "privacy_breached": "unknown",
            "second_opinion_denied": "unknown",
            "billing_issue": "unknown",
            "discrimination_claimed": "unknown",

            # -----------------------------
            # IMC absolute duty
            # -----------------------------
            "doctor_under_influence": "no",

            # -----------------------------
            # PROCEDURAL REMEDY FLAGS
            # -----------------------------
            "mistreatment_claimed": "no",
            "abuse_claimed": "no",
            "unethical_behavior_claimed": "no",

            # -----------------------------
            # Medical records
            # -----------------------------
            "records_issue": {
                "requested": "unknown",
                "denied": "unknown",
                "by_doctor": "unknown",
                "by_hospital": "unknown"
            }
        }

        # =====================================================
        # Actor detection
        # =====================================================
        if "doctor" in text:
            facts["doctor_involved"] = "yes"

        if "hospital" in text:
            facts["hospital_involved"] = "yes"

        # =====================================================
        # Emergency detection
        # =====================================================
        if re.search(r"(emergency|urgent|critical|life threatening)", text):
            facts["emergency_claimed"] = "yes"

        if re.search(
            r"(accident|car accident|road accident|bleeding|unconscious|injured)",
            text
        ):
            facts["emergency_case"] = "yes"

        # =====================================================
        # Treatment refusal
        # =====================================================
        if re.search(
            r"(refused|deny|denied|did not treat|no treatment|ignored)",
            text
        ):
            facts["treatment_refused"] = "yes"

        # =====================================================
        # Admission denied
        # =====================================================
        if re.search(
            r"(denied admission|denied to admit|refused admission|refused to admit|not admitted|not allowed to admit)",
            text
        ):
            facts["admission_denied"] = "yes"

        # =====================================================
        # Payment demanded
        # =====================================================
        if re.search(
            r"(ask|asked|asking).*(payment|money|fees)|full payment|payment first|pay first|fees first|advance payment",
            text
        ):
            facts["payment_demanded"] = "yes"

        # =====================================================
        # Medical records
        # =====================================================
        if re.search(
            r"(report|records|test results|file|medical papers|discharge summary)",
            text
        ):
            facts["records_issue"]["requested"] = "yes"

        if re.search(r"(refused|denied|withheld|not sharing)", text):
            if facts["records_issue"]["requested"] == "yes":
                facts["records_issue"]["denied"] = "yes"

        if re.search(r"(did not give|not given|still waiting|even after asking)", text):
            if facts["records_issue"]["requested"] == "yes":
                facts["records_issue"]["denied"] = "yes"

        if facts["doctor_involved"] == "yes":
            facts["records_issue"]["by_doctor"] = "yes"

        if facts["hospital_involved"] == "yes":
            facts["records_issue"]["by_hospital"] = "yes"

        # =====================================================
        # Informed consent
        # =====================================================
        if re.search(r"(without consent|no consent|did not explain)", text):
            facts["consent_issue"] = "yes"

        if re.search(r"(surgery|procedure|operation)", text) and re.search(
            r"(without|no|not explained|did not|not told)", text
        ):
            facts["consent_issue"] = "yes"

        # =====================================================
        # Privacy breach
        # =====================================================
        if re.search(
            r"(shared|discussed).*(medical|condition|information)|without my permission|in front of others|loudly",
            text
        ):
            facts["privacy_breached"] = "yes"

        # =====================================================
        # Second opinion denied
        # =====================================================
        if re.search(r"(second opinion|another doctor|consult another)", text) and re.search(
            r"(refused|not allowed|stopped|denied)",
            text
        ):
            facts["second_opinion_denied"] = "yes"

        # =====================================================
        # Billing transparency
        # =====================================================
        if re.search(r"(charges|bill|fees)", text) and re.search(
            r"(hidden|sudden|changed|not informed)",
            text
        ):
            facts["billing_issue"] = "yes"

        # =====================================================
        # Discrimination
        # =====================================================
        if re.search(
            r"(discriminated|treated differently|because of caste|religion|gender)",
            text
        ):
            facts["discrimination_claimed"] = "yes"

        # =====================================================
        # Doctor under influence
        # =====================================================
        if re.search(r"(drunk|intoxicated|alcohol|under the influence|high)", text):
            if facts["doctor_involved"] == "yes":
                facts["doctor_under_influence"] = "yes"

        # =====================================================
        # PROCEDURAL REMEDY CLAIMS (FIXED)
        # =====================================================
        if re.search(
            r"(mistreated|mistreatment|treated badly|bad behaviour|bad behavior)",
            text
        ):
            facts["mistreatment_claimed"] = "yes"

        if re.search(
            r"(abuse|abused|abusing|shout|shouted|shouting|insult|insulted|insulting|threaten|threatened)",
            text
        ):
            facts["abuse_claimed"] = "yes"

        if re.search(r"(unethical|irresponsible|wrong conduct)", text):
            facts["unethical_behavior_claimed"] = "yes"

        return facts

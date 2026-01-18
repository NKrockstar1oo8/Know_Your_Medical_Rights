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
            "information_denied": "unknown",
            "billing_not_explained": "unknown",
            "doctor_identity_not_disclosed": "unknown",

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
            "rates_not_disclosed": "unknown",
            "overcharging_claimed": "unknown",
            "forced_payment_claimed": "unknown",
            "billing_coercion_claimed": "unknown",
            "discrimination_claimed": "unknown",
            "discrimination_basis": "unknown",
            "discharge_denied": "unknown",
            "patient_detained_for_payment": "unknown",
            "body_withheld_for_payment": "unknown",
            "unsafe_conditions_claimed": "unknown",
            "hygiene_failure_claimed": "unknown",
            "infection_due_to_care_claimed": "unknown",
            "negligence_claimed": "unknown",
            "substandard_care_claimed": "unknown",
            "second_opinion_denied": "unknown",
            "pressure_against_second_opinion": "unknown",
            "records_withheld_for_second_opinion": "unknown",
            "forced_pharmacy_claimed": "unknown",
            "forced_diagnostic_lab_claimed": "unknown",
            "penalty_for_external_source_claimed": "unknown",
            "treatment_choice_denied": "unknown",
            "forced_treatment_claimed": "unknown",
            "refusal_not_allowed_claimed": "unknown",
            "coercion_for_treatment_claimed": "unknown",
            "penalty_for_refusal_claimed": "unknown",
            "referral_denied_claimed": "unknown",
            "transfer_without_explanation_claimed": "unknown",
            "unsafe_transfer_claimed": "unknown",
            "commercial_referral_claimed": "unknown",
            "lack_of_continuity_of_care_claimed": "unknown",
            "grievance_denied_claimed": "unknown",
            "complaint_ignored_claimed": "unknown",
            "retaliation_for_complaint_claimed": "unknown",
            "no_grievance_mechanism_claimed": "unknown",
            "patient_education_denied_claimed": "unknown",
            "language_barrier_claimed": "unknown",
            "rights_not_explained_claimed": "unknown",
            "information_not_understandable_claimed": "unknown",
            
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

        # -------------------------------------------------
        # RIGHT TO PATIENT EDUCATION — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "no education given",
            "not educated about condition",
            "no information about care",
            "no explanation about treatment"
        ]):
            facts["patient_education_denied_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "language barrier",
            "could not understand language",
            "no explanation in my language",
            "explained in a language we don't understand"
        ]):
            facts["language_barrier_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "rights not explained",
            "not told about patient rights",
            "no information about patient rights",
            "rights were not explained"
        ]):
            facts["rights_not_explained_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "information not understandable",
            "too technical to understand",
            "could not understand explanation",
            "explanation was confusing"
        ]):
            facts["information_not_understandable_claimed"] = "yes"


        # -------------------------------------------------
        # RIGHT TO BE HEARD & SEEK REDRESSAL — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "complaint not accepted",
            "grievance denied",
            "not allowed to complain",
            "refused to take complaint"
        ]):
            facts["grievance_denied_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "complaint ignored",
            "no response to complaint",
            "nobody listened to complaint",
            "no action on complaint"
        ]):
            facts["complaint_ignored_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "retaliation for complaint",
            "threatened after complaint",
            "treatment worsened after complaint",
            "harassed for complaining"
        ]):
            facts["retaliation_for_complaint_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "no grievance cell",
            "no complaint mechanism",
            "no system to complain",
            "hospital has no grievance mechanism"
        ]):
            facts["no_grievance_mechanism_claimed"] = "yes"


        # -------------------------------------------------
        # RIGHT TO PROPER REFERRAL & TRANSFER — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "referral denied",
            "doctor refused referral",
            "not referred despite lack of facility",
            "refused to refer"
        ]):
            facts["referral_denied_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "transferred without explanation",
            "no explanation for transfer",
            "suddenly transferred",
            "shifted without reason"
        ]):
            facts["transfer_without_explanation_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "unsafe transfer",
            "no ambulance support",
            "transferred without oxygen",
            "no medical support during transfer"
        ]):
            facts["unsafe_transfer_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "referred for commission",
            "commercial referral",
            "sent for money",
            "referred for financial benefit"
        ]):
            facts["commercial_referral_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "no records sent",
            "records not transferred",
            "treatment stopped during transfer",
            "no continuity of care"
        ]):
            facts["lack_of_continuity_of_care_claimed"] = "yes"


        # -------------------------------------------------
        # RIGHT TO CHOOSE TREATMENT OPTIONS — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "no choice of treatment",
            "treatment choice denied",
            "not allowed to choose treatment",
            "only one treatment forced"
        ]):
            facts["treatment_choice_denied"] = "yes"

        if any(phrase in text for phrase in [
            "forced treatment",
            "treatment forced",
            "treatment done without consent",
            "given treatment against will"
        ]):
            facts["forced_treatment_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "not allowed to refuse treatment",
            "refusal not allowed",
            "doctor said cannot refuse",
            "cannot refuse treatment"
        ]):
            facts["refusal_not_allowed_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "pressured to accept treatment",
            "coerced into treatment",
            "threatened if treatment refused",
            "forced to accept treatment"
        ]):
            facts["coercion_for_treatment_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "treatment stopped because refused",
            "penalized for refusing treatment",
            "threatened discharge for refusing treatment",
            "punished for refusing treatment"
        ]):
            facts["penalty_for_refusal_claimed"] = "yes"

        # -------------------------------------------------
        # RIGHT TO CHOOSE SOURCE FOR MEDICINES & TESTS — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "forced to buy medicines",
            "forced to buy medicine",
            "hospital pharmacy compulsory",
            "not allowed to buy medicines outside",
            "only hospital pharmacy allowed"
        ]):
            facts["forced_pharmacy_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "forced to do tests in hospital",
            "forced hospital lab",
            "only hospital lab allowed",
            "not allowed external lab",
            "diagnostic tests only here"
        ]):
            facts["forced_diagnostic_lab_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "penalized for buying outside",
            "treatment delayed because medicines bought outside",
            "refused care after buying medicines outside",
            "problem because tests done outside"
        ]):
            facts["penalty_for_external_source_claimed"] = "yes"


        # -------------------------------------------------
        # RIGHT TO SECOND OPINION — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "second opinion denied",
            "not allowed second opinion",
            "refused second opinion",
            "not allowed to consult another doctor"
        ]):
            facts["second_opinion_denied"] = "yes"

        if any(phrase in text for phrase in [
            "discouraged second opinion",
            "pressured not to seek second opinion",
            "told not to take second opinion",
            "threatened for second opinion"
        ]):
            facts["pressure_against_second_opinion"] = "yes"

        if any(phrase in text for phrase in [
            "records not given for second opinion",
            "reports withheld for second opinion",
            "documents refused for second opinion"
        ]):
            facts["records_withheld_for_second_opinion"] = "yes"


        # -------------------------------------------------
        # RIGHT TO SAFETY & QUALITY CARE — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "unsafe hospital",
            "unsafe conditions",
            "dangerous conditions",
            "no safety measures",
            "unsafe equipment"
        ]):
            facts["unsafe_conditions_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "no hygiene",
            "dirty ward",
            "unsanitary conditions",
            "poor cleanliness",
            "lack of hygiene"
        ]):
            facts["hygiene_failure_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "hospital acquired infection",
            "got infected in hospital",
            "infection due to hospital",
            "infection due to care"
        ]):
            facts["infection_due_to_care_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "negligence",
            "negligent",
            "carelessness",
            "gross negligence"
        ]):
            facts["negligence_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "substandard care",
            "below standard care",
            "improper treatment",
            "not as per standards"
        ]):
            facts["substandard_care_claimed"] = "yes"


        # -------------------------------------------------
        # RIGHT TO DISCHARGE & BODY OF DECEASED — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "discharge denied",
            "refused to discharge",
            "not allowing discharge",
            "discharge papers not given"
        ]):
            facts["discharge_denied"] = "yes"

        if any(phrase in text for phrase in [
            "patient detained",
            "not allowed to leave",
            "detained for payment",
            "kept in hospital for bill",
            "held until payment"
        ]):
            facts["patient_detained_for_payment"] = "yes"

        if any(phrase in text for phrase in [
            "body not released",
            "body withheld",
            "dead body withheld",
            "refused to hand over body",
            "body kept due to bill"
        ]):
            facts["body_withheld_for_payment"] = "yes"


        # -------------------------------------------------
        # RIGHT TO NON-DISCRIMINATION — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "discriminated",
            "discrimination",
            "treated differently because",
            "refused because",
            "denied because"
        ]):
            facts["discrimination_claimed"] = "yes"

            # Capture descriptive basis ONLY if explicitly mentioned
            if any(word in text for word in ["religion", "religious"]):
                facts["discrimination_basis"] = "religion"
            elif "caste" in text:
                facts["discrimination_basis"] = "caste"
            elif any(word in text for word in ["gender", "woman", "female", "male"]):
                facts["discrimination_basis"] = "gender"
            elif any(word in text for word in ["age", "old", "elderly", "minor"]):
                facts["discrimination_basis"] = "age"
            elif any(word in text for word in ["poor", "poverty", "economic", "money"]):
                facts["discrimination_basis"] = "economic_status"
            elif any(word in text for word in ["hiv", "aids", "illness", "disease"]):
                facts["discrimination_basis"] = "illness"
            elif any(word in text for word in ["disability", "disabled"]):
                facts["discrimination_basis"] = "disability"


        # -------------------------------------------------
        # RIGHT TO TRANSPARENCY IN RATES & CARE — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "rates not disclosed",
            "rate list not shown",
            "charges not disclosed",
            "price not told",
            "cost not told in advance",
            "no rate list"
        ]):
            facts["rates_not_disclosed"] = "yes"

        if any(phrase in text for phrase in [
            "overcharged",
            "charged extra",
            "excessive charges",
            "unreasonable charges",
            "more than allowed",
            "inflated bill"
        ]):
            facts["overcharging_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "asked for advance",
            "advance payment demanded",
            "forced to pay",
            "payment demanded first",
            "treatment denied without payment"
        ]):
            facts["forced_payment_claimed"] = "yes"

        if any(phrase in text for phrase in [
            "detained for bill",
            "body not released",
            "pressured for payment",
            "threatened discharge",
            "billing pressure"
        ]):
            facts["billing_coercion_claimed"] = "yes"


        # -------------------------------------------------
        # RIGHT TO INFORMATION — NHRC (2019)
        # -------------------------------------------------

        if any(phrase in text for phrase in [
            "not explained",
            "no explanation",
            "did not explain",
            "nothing was explained",
            "no information given",
            "not informed"
        ]):
            facts["information_denied"] = "yes"

        if any(phrase in text for phrase in [
            "bill not explained",
            "charges not explained",
            "sudden charges",
            "hidden charges",
            "no cost information",
            "billing not explained"
        ]):
            facts["billing_not_explained"] = "yes"

        if any(phrase in text for phrase in [
            "doctor name not told",
            "doctor identity not disclosed",
            "do not know which doctor",
            "no doctor name",
            "identity not disclosed"
        ]):
            facts["doctor_identity_not_disclosed"] = "yes"

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

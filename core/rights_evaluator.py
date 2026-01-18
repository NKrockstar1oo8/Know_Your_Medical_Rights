# core/rights_evaluator.py

class RightsEvaluator:
    def evaluate(self, facts: dict) -> dict:

        provable = []          # NHRC patient rights
        imc_duties = []        # IMC doctor duties
        procedural = []        # Procedural (non-advisory)

        emergency_violation = False

        # -------------------------------------------------
        # Helper: prevent duplicate IMC duties
        # -------------------------------------------------
        def add_imc_duty(duty: dict):
            if duty["id"] not in {d["id"] for d in imc_duties}:
                imc_duties.append(duty)

        # =====================================================
        # NHRC-01 — Right to Information
        # =====================================================
        if (
            facts.get("information_denied") == "yes"
            or facts.get("billing_not_explained") == "yes"
            or facts.get("doctor_identity_not_disclosed") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_INFORMATION",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 1",
                "explanation": [
                    "Patients have the right to receive clear information about diagnosis and treatment.",
                    "Patients have the right to be informed about expected costs.",
                    "Patients have the right to know the identity of treating doctors."
                ]
            })

        # =====================================================
        # NHRC-02 — Records & Reports (+ IMC 1.3)
        # =====================================================
        records = facts.get("records_issue", {})
        if records.get("requested") == "yes" and records.get("denied") == "yes":
            provable.append({
                "id": "RIGHT_TO_RECORDS_AND_REPORTS",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Clause 2",
                "explanation": [
                    "Patients have the right to access their medical records.",
                    "Hospitals must provide records within prescribed timelines."
                ]
            })

            if facts.get("doctor_involved") == "yes":
                add_imc_duty({
                    "id": "DUTY_TO_MAINTAIN_AND_PROVIDE_MEDICAL_RECORDS",
                    "source": "IMC_2002",
                    "citation": (
                        "Indian Medical Council (Professional Conduct, Etiquette and Ethics) "
                        "Regulations, 2002, Chapter 1, Clause 1.3"
                    ),
                    "explanation": [
                        "A physician must maintain proper medical records.",
                        "Records must be provided to patients as per regulations."
                    ]
                })

        # =====================================================
        # NHRC-03 — Emergency Medical Care (+ IMC 2.1.1)
        # =====================================================
        if (
            (facts.get("emergency_case") == "yes" or facts.get("emergency_claimed") == "yes")
            and (
                facts.get("treatment_refused") == "yes"
                or facts.get("admission_denied") == "yes"
                or facts.get("payment_demanded") == "yes"
            )
        ):
            emergency_violation = True

            provable.append({
                "id": "RIGHT_TO_EMERGENCY_MEDICAL_CARE",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Clause 3",
                "explanation": [
                    "Emergency medical care must not be delayed or denied.",
                    "Refusal or conditional treatment based on payment violates patient rights."
                ]
            })

            if facts.get("doctor_involved") == "yes":
                add_imc_duty({
                    "id": "DUTY_TO_PROVIDE_EMERGENCY_CARE",
                    "source": "IMC_2002",
                    "citation": (
                        "Indian Medical Council (Professional Conduct, Etiquette and Ethics) "
                        "Regulations, 2002, Chapter 2, Clause 2.1.1"
                    ),
                    "explanation": [
                        "A physician has a duty to respond to medical emergencies.",
                        "Emergency care must not be refused or delayed."
                    ]
                })

        # =====================================================
        # NHRC-04 — Informed Consent (+ IMC 3.1)
        # =====================================================
        if facts.get("consent_issue") == "yes":
            provable.append({
                "id": "RIGHT_TO_INFORMED_CONSENT",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Clause 4",
                "explanation": [
                    "Informed consent is mandatory before risky procedures.",
                    "Risks and alternatives must be explained."
                ]
            })

            if facts.get("doctor_involved") == "yes":
                add_imc_duty({
                    "id": "DUTY_TO_OBTAIN_INFORMED_CONSENT",
                    "source": "IMC_2002",
                    "citation": (
                        "Indian Medical Council (Professional Conduct, Etiquette and Ethics) "
                        "Regulations, 2002, Chapter 3, Clause 3.1"
                    ),
                    "explanation": [
                        "A physician must obtain informed consent before procedures.",
                        "Risks, benefits, and alternatives must be explained."
                    ]
                })

        # =====================================================
        # NHRC-06 — Second Opinion
        # =====================================================
        if (
            facts.get("second_opinion_denied") == "yes"
            or facts.get("pressure_against_second_opinion") == "yes"
            or facts.get("records_withheld_for_second_opinion") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_SECOND_OPINION",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 6",
                "explanation": [
                    "Patients have the right to seek a second medical opinion regarding their diagnosis or treatment.",
                    "Patients have the right to receive necessary medical records to obtain a second opinion.",
                    "Patients must not be discriminated against or pressured for seeking a second opinion."
                ]
            })

        # =====================================================
        # NHRC-07 — Transparency in Rates
        # =====================================================
        if (
            facts.get("rates_not_disclosed") == "yes"
            or facts.get("overcharging_claimed") == "yes"
            or facts.get("forced_payment_claimed") == "yes"
            or facts.get("billing_coercion_claimed") == "yes"
            or facts.get("billing_not_explained") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_TRANSPARENCY_IN_RATES_AND_CARE",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 7",
                "explanation": [
                    "Patients have the right to transparency in hospital rates and charges.",
                    "Patients have the right to receive itemized bills.",
                    "Patients must not be denied or pressured for care based on ability to pay."
                ]
            })

        # =====================================================
        # NHRC-08 — Non-Discrimination
        # =====================================================
        if facts.get("discrimination_claimed") == "yes":
            provable.append({
                "id": "RIGHT_TO_NON_DISCRIMINATION",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 8",
                "explanation": [
                    "Patients have the right to receive medical care without discrimination.",
                    "Discrimination on grounds such as religion, caste, gender, age, disability, or illness is prohibited.",
                    "Medical care must be based on clinical need."
                ]
            })

        # =====================================================
        # NHRC-09 — Safety & Quality Care (+ IMC 2.1.4)
        # =====================================================
        if (
            facts.get("unsafe_conditions_claimed") == "yes"
            or facts.get("hygiene_failure_claimed") == "yes"
            or facts.get("infection_due_to_care_claimed") == "yes"
            or facts.get("negligence_claimed") == "yes"
            or facts.get("substandard_care_claimed") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_SAFETY_AND_QUALITY_CARE",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 9",
                "explanation": [
                    "Patients have the right to receive safe and quality medical care.",
                    "Hospitals must ensure hygiene, infection control, and patient safety.",
                    "Medical care must be provided according to accepted standards of practice."
                ]
            })

            if facts.get("doctor_involved") == "yes":
                add_imc_duty({
                    "id": "DUTY_TO_PROVIDE_COMPETENT_AND_ETHICAL_CARE",
                    "source": "IMC_2002",
                    "citation": (
                        "Indian Medical Council (Professional Conduct, Etiquette and Ethics) "
                        "Regulations, 2002, Chapter 2, Clause 2.1.4"
                    ),
                    "explanation": [
                        "A physician must provide medical care with reasonable skill and competence.",
                        "Care must conform to accepted standards of medical practice."
                    ]
                })

        # =====================================================
        # NHRC-10 — Choice of Treatment
        # =====================================================
        if (
            facts.get("treatment_choice_denied") == "yes"
            or facts.get("forced_treatment_claimed") == "yes"
            or facts.get("refusal_not_allowed_claimed") == "yes"
            or facts.get("coercion_for_treatment_claimed") == "yes"
            or facts.get("penalty_for_refusal_claimed") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_CHOOSE_TREATMENT_OPTIONS",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 10",
                "explanation": [
                    "Patients have the right to choose among available treatment options after being informed.",
                    "Patients have the right to refuse treatment after being informed of consequences.",
                    "Patients must not be coerced or penalized for refusing or choosing a particular treatment."
                ]
            })

        # =====================================================
        # NHRC-11 — Medicines & Tests
        # =====================================================
        if (
            facts.get("forced_pharmacy_claimed") == "yes"
            or facts.get("forced_diagnostic_lab_claimed") == "yes"
            or facts.get("penalty_for_external_source_claimed") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_CHOOSE_SOURCE_FOR_MEDICINES_AND_TESTS",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 11",
                "explanation": [
                    "Patients have the right to choose where to purchase medicines.",
                    "Patients have the right to choose where to obtain diagnostic tests from accredited centres.",
                    "Patients must not be forced or penalized for choosing medicines or tests from an external source."
                ]
            })

        # =====================================================
        # NHRC-12 — Referral & Transfer
        # =====================================================
        if (
            facts.get("referral_denied_claimed") == "yes"
            or facts.get("transfer_without_explanation_claimed") == "yes"
            or facts.get("unsafe_transfer_claimed") == "yes"
            or facts.get("commercial_referral_claimed") == "yes"
            or facts.get("lack_of_continuity_of_care_claimed") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_PROPER_REFERRAL_AND_TRANSFER",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 12",
                "explanation": [
                    "Patients have the right to appropriate and timely referral or transfer when required.",
                    "Patients have the right to receive clear reasons for referral or transfer.",
                    "Referral and transfer must ensure continuity of care and patient safety."
                ]
            })

        # =====================================================
        # NHRC-15 — Discharge & Body
        # =====================================================
        if (
            facts.get("discharge_denied") == "yes"
            or facts.get("patient_detained_for_payment") == "yes"
            or facts.get("body_withheld_for_payment") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_DISCHARGE_AND_BODY_OF_DECEASED",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 15",
                "explanation": [
                    "Patients have the right to be discharged when medically fit or on request.",
                    "Hospitals must not detain patients due to non-payment of charges.",
                    "Hospitals must not withhold the body of the deceased due to billing disputes."
                ]
            })

        # =====================================================
        # NHRC-16 — Patient Education
        # =====================================================
        if (
            facts.get("patient_education_denied_claimed") == "yes"
            or facts.get("language_barrier_claimed") == "yes"
            or facts.get("rights_not_explained_claimed") == "yes"
            or facts.get("information_not_understandable_claimed") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_PATIENT_EDUCATION",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 16",
                "explanation": [
                    "Patients have the right to receive education and information about their health and care.",
                    "Patients have the right to be informed about their rights and responsibilities.",
                    "Information should be communicated in a language and manner that the patient can understand."
                ]
            })

        # =====================================================
        # NHRC-17 — Grievance Redressal
        # =====================================================
        if (
            facts.get("grievance_denied_claimed") == "yes"
            or facts.get("complaint_ignored_claimed") == "yes"
            or facts.get("retaliation_for_complaint_claimed") == "yes"
            or facts.get("no_grievance_mechanism_claimed") == "yes"
        ):
            provable.append({
                "id": "RIGHT_TO_BE_HEARD_AND_SEEK_REDRESSAL",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Right 17",
                "explanation": [
                    "Patients have the right to raise complaints and grievances regarding medical care.",
                    "Patients have the right to have their complaints heard and addressed through institutional mechanisms.",
                    "Patients must not face discrimination or retaliation for raising grievances."
                ]
            })

        # =====================================================
        # IMC 2.1.2 — Under Influence
        # =====================================================
        if facts.get("doctor_under_influence") == "yes":
            add_imc_duty({
                "id": "DUTY_NOT_TO_PRACTICE_UNDER_INFLUENCE",
                "source": "IMC_2002",
                "citation": (
                    "Indian Medical Council (Professional Conduct, Etiquette and Ethics) "
                    "Regulations, 2002, Chapter 2, Clause 2.1.2"
                ),
                "explanation": [
                    "A physician must not practice medicine under the influence of alcohol or drugs.",
                    "Practicing under such influence constitutes professional misconduct."
                ]
            })

        # =====================================================
        # PROCEDURAL — Descriptive only (NO ADVICE)
        # =====================================================
        if facts.get("doctor_involved") == "yes":
            if (
                facts.get("mistreatment_claimed") == "yes"
                or facts.get("abuse_claimed") == "yes"
                or facts.get("unethical_behavior_claimed") == "yes"
            ):
                procedural.append({
                    "id": "PROFESSIONAL_CONDUCT_CONCERNS",
                    "source": "IMC_2002",
                    "citation": "Indian Medical Council Regulations, 2002",
                    "explanation": [
                        "Doctors are required to maintain professional conduct and dignity.",
                        "Unethical or abusive behaviour is regulated under medical ethics standards."
                    ]
                })

        # =====================================================
        # FINAL VERDICT
        # =====================================================
        if provable or imc_duties or procedural:
            if provable or imc_duties:
                verdict_type = "PROVABLE"
            else:
                verdict_type = "PROCEDURAL"

            return {
                "verdict_type": verdict_type,
                "primary_violations": provable,
                "imc_duties": imc_duties,
                "procedural_remedies": procedural
            }


        return {
            "verdict_type": "NOT_PROVABLE",
            "reasons": [
                "No legally decidable right or duty applies.",
                "The system cannot reach a determination based on the provided information."
            ]
        }

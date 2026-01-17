# core/rights_evaluator.py

class RightsEvaluator:
    def evaluate(self, facts: dict) -> dict:

        provable = []
        procedural = []

        # =====================================================
        # RULE 1 — Emergency medical care (NHRC Clause 3)
        # =====================================================
        if (
            (
                facts.get("emergency_case") == "yes"
                or facts.get("emergency_claimed") == "yes"
            )
            and (
                facts.get("treatment_refused") == "yes"
                or facts.get("admission_denied") == "yes"
            )
        ):
            provable.append({
                "id": "RIGHT_TO_EMERGENCY_MEDICAL_CARE",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Clause 3",
                "explanation": [
                    "Emergency medical care must not be delayed or denied.",
                    "Refusal of treatment or admission in an emergency violates patient rights."
                ]
            })

        # =====================================================
        # RULE 2 — Doctor under influence (IMC Clause 2.1.2)
        # =====================================================
        if facts.get("doctor_under_influence") == "yes":
            provable.append({
                "id": "DUTY_NOT_TO_PRACTICE_UNDER_INFLUENCE",
                "source": "IMC_2002",
                "citation": (
                    "Indian Medical Council (Professional Conduct, Etiquette and Ethics) "
                    "Regulations, 2002, Chapter 2, Clause 2.1.2"
                ),
                "explanation": [
                    "Doctors must not practice under the influence of alcohol or drugs.",
                    "This constitutes professional misconduct."
                ]
            })

        # =====================================================
        # RULE 3 — Informed consent
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

        # =====================================================
        # RULE 4 — Records denied
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

        # =====================================================
        # RULE 5 — Privacy breach
        # =====================================================
        if facts.get("privacy_breached") == "yes":
            provable.append({
                "id": "RIGHT_TO_PRIVACY_AND_CONFIDENTIALITY",
                "source": "NHRC_2019",
                "citation": "Charter of Patients’ Rights (NHRC, 2019), Clause 5",
                "explanation": [
                    "Medical information must remain confidential.",
                    "Patient dignity and privacy must be respected."
                ]
            })

        # =====================================================
        # PROCEDURAL REMEDIES — Doctor behaviour
        # =====================================================
        if facts.get("doctor_involved") == "yes":
            if (
                facts.get("mistreatment_claimed") == "yes"
                or facts.get("abuse_claimed") == "yes"
                or facts.get("unethical_behavior_claimed") == "yes"
            ):
                procedural.append({
                    "id": "PROFESSIONAL_MISCONDUCT_BY_DOCTOR",
                    "source": "IMC_2002",
                    "citation": (
                        "Indian Medical Council (Professional Conduct, Etiquette and Ethics) "
                        "Regulations, 2002"
                    ),
                    "explanation": [
                        "Doctors must maintain dignity and professional conduct.",
                        "Abusive or unethical behaviour may amount to misconduct.",
                        "A complaint can be filed with the State Medical Council."
                    ]
                })

                procedural.append({
                    "id": "RIGHT_TO_GRIEVANCE_REDRESSAL",
                    "source": "NHRC_2019",
                    "citation": "Charter of Patients’ Rights (NHRC, 2019), Clause 17",
                    "explanation": [
                        "Patients have the right to file grievances.",
                        "Hospitals must provide grievance redressal mechanisms."
                    ]
                })

        # =====================================================
        # FINAL DECISION
        # =====================================================
        if provable or procedural:
            return {
                "verdict_type": "PROVABLE" if provable else "PROCEDURAL_REMEDY_AVAILABLE",
                "primary_violations": provable,
                "procedural_remedies": procedural
            }

        return {
            "verdict_type": "NOT_PROVABLE",
            "reasons": [
                "No legally decidable right or duty applies.",
                "The system cannot reach a legal conclusion."
            ]
        }

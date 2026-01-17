from enum import Enum

class EntityType(Enum):
    PERSON = "person"
    MEDICAL_PROFESSIONAL = "medical_professional"
    PATIENT = "patient"
    INSTITUTION = "institution"
    DOCUMENT = "document"
    ACT = "act"
    SECTION = "section"
    MEDICAL_PROCEDURE = "medical_procedure"

class RelationType(Enum):
    GOVERNED_BY = "governed_by"
    HAS_SECTION = "has_section"
    REQUIRES_CONSENT = "requires_consent"
    PERFORMED_BY = "performed_by"
    APPLIES_TO = "applies_to"

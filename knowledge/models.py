from dataclasses import dataclass

@dataclass(frozen=True)
class LegalEntity:
    id: str
    type: str
    name: str
@dataclass(frozen=True)
class LegalRelation:
    subject_id: str
    relation: str
    object_id: str
@dataclass(frozen=True)
class LegalFact:
    entity: LegalEntity

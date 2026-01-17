def load_knowledge(path):
    data = load_json(path)

    assert "entities" in data
    assert "relations" in data

    entity_ids = set()

    for entity in data["entities"]:
        validate_entity_schema(entity)
        entity_ids.add(entity["id"])

    for relation in data["relations"]:
        validate_relation_schema(relation)
        assert relation["subject_id"] in entity_ids
        assert relation["object_id"] in entity_ids

    return InMemoryGraph(entities, relations)

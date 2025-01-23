class DataMapper:
    db_model = None
    schema = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(
            data, from_attributes=True
        )  # Из Алхимии в pydantic схему

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())  # Из схемы в объект алхимии

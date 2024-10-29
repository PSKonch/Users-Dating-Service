from typing import TypeVar
from pydantic import BaseModel

from src.db import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


# DataMapper нам необходим, чтобы возвращать pydantic схему вместо сущности в бд
# Таким образом мы изолируем базу данных от бизнес логики при get запросах
class DataMapper:
    db_model = None
    schema = None
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
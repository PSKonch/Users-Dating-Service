from src.repositories.mappers.base import DataMapper
from src.models.clients import ClientsModel
from src.schemas.clients import Client

class ClientsDataMapper(DataMapper):
    db_model = ClientsModel
    schema = Client
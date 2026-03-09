from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ComentarioCreate(BaseModel):
    texto: str

class ComentarioUpdate(BaseModel):
    texto: str

# NOTE: This model is used for ORM objects; from_attributes lets pydantic read SQLAlchemy instances.
class ComentarioOut(BaseModel):
    id: int
    texto: str
    data_criacao: datetime
    usuario_id: int
    tarefa_id: int

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel
from datetime import datetime

class LogOut(BaseModel):
    id: int
    acao: str
    descricao: str | None
    data: datetime

    class Config:
        from_attributes = True
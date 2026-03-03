from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.tarefa import StatusTarefa


class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    status: Optional[StatusTarefa] = StatusTarefa.pendente


class TarefaCreate(TarefaBase):
    pass


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusTarefa] = None


class TarefaOut(TarefaBase):
    id: int
    projeto_id: int
    usuario_id: int
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True
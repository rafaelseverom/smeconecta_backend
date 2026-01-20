# Esse schema define como os dados entram e saem pela API

from pydantic import BaseModel
from typing import Optional
from app.core.enums import StatusProjeto


class ProjetoBase(BaseModel):
    nome: str
    descricao: str
    status: Optional[StatusProjeto] = StatusProjeto.ativo

class ProjetoCreate(ProjetoBase):
    pass

class ProjetoUpdate(ProjetoBase):
    pass

class ProjetoOut(ProjetoBase):
    id: int

    class Config:
        from_attributes = True

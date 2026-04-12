# Esse schema define como os dados entram e saem pela API

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.core.enums import StatusProjeto
from typing import List
from pydantic import BaseModel

class ProjetoCreate(BaseModel):
    nome: str
    descricao: str
    teacher_ids: List[int] = []

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
    model_config = ConfigDict(from_attributes=True)

class TeacherResumo(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProjetoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    teachers: List[TeacherResumo] = []

class ProjetoOut(BaseModel):
    id: int
    nome: str
    descricao: str
    status: str
    teachers: List[TeacherResumo] = []

    class Config:
        from_attributes = True
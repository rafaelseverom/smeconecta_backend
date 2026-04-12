from pydantic import BaseModel
from typing import Optional
from datetime import date


class TeacherBase(BaseModel):
    name: str
    cpf: str
    telefone: Optional[str] = None
    genero: Optional[str] = None
    funcao: Optional[str] = None

    temporary: bool = False
    outsource: bool = False
    status: bool = True

    data_ativacao: Optional[date] = None
    data_desativacao: Optional[date] = None


class TeacherCreate(TeacherBase):
    pass


class TeacherResponse(TeacherBase):
    id: int

    class Config:
        from_attributes = True
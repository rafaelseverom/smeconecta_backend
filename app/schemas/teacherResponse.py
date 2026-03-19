from pydantic import BaseModel
from datetime import date

class TeacherBase(BaseModel):
    id: int
    name: str
    cpf : str
    temporary: bool
    outsource: bool
    status : bool
    funcao : str
    
class Teacher(BaseModel):
    id: int
    name: str
    temporary: bool
    outsource: bool
    
    # Dado pessoal
    cpf: str
    telefone : str
    genero : str
    nasc : date
    qtd_filhos : int

    # Função
    funcao : str
    data_ativacao : date | None = None
    data_desativacao : date | None = None

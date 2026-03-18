from fastapi import APIRouter

from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.teacherResponse import TeacherBase
from app.schemas.teacherResponse import Teacher
from app.schemas.pagination import Page

from app.utils.pagination import paginate

from app.core.database import get_teachers_from_DB
from app.core.database import get_teacher_by_id


#   Implementar rotas relacionada a usuários
router = APIRouter(prefix="/teacher", tags=["Teacher"])

# GET /teachers          → lista com filtros
# GET /teachers/{id}     → detalhe
# POST /teachers         → criar
# PUT /teachers/{id}     → atualizar
# DELETE /teachers/{id}  → deletar

# GET /employees
# @router.get("/{id}", response_model=TeacherBase)
# def root(id: int):
#     teachers_db = get_teachers_from_DB()

#     for i in teachers_db:
#         if i.id == id:
#             return i
        
#     raise HTTPException(status_code=404, detail="Teacher not found")


@router.get("/", response_model=Page[TeacherBase])
def listTeachers(
    search: Optional[str] = None,
    type: Optional[str] = "todos",
    status: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):

    teachers_db = get_teachers_from_DB()
    results = teachers_db

    type = type.lower() if type else "todos"
    status = status.lower() if status else None

    # SEARCH
    if search:
        s = search.lower()
        results = [
            t for t in results
            if s in t.name.lower() or s in t.cpf or s in t.funcao.lower()
        ]

    # TYPE
    if type.lower() == "temporarios":
        results = [t for t in results if t.temporary]
    
    elif type.lower() == "tercerizados":
        results = [t for t in results if t.outsource]
    
    elif type.lower() == "concursados":
        results = [
            t for t in results
            if not t.temporary and not t.outsource
        ]

    # STATUS
    if status == "ativo":
        results = [t for t in results if t.status]

    elif status == "inativo":
        results = [t for t in results if not t.status]

    return paginate(results, page, limit)

@router.get("/{id}", response_model=Teacher)
def get_teacher(id: int):
    
    teacher = get_teacher_by_id(id)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Professor não encontrado"
        )

    return teacher
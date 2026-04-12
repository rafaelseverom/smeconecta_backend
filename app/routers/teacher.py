from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherResponse
from app.utils.pagination import paginate
from app.schemas.pagination import Page
from app.core.security import get_usuario_logado
from app.models.usuario import Usuario
from app.schemas.tipo_teacher import TipoTeacher
from datetime import date
from sqlalchemy import asc, desc
router = APIRouter(prefix="/teacher", tags=["Teacher"])


# CREATE
@router.post("/", response_model=TeacherResponse)
def create_teacher(
    teacher: TeacherCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    db_teacher = Teacher(**teacher.model_dump())
    
    db_teacher.usuario_id = usuario.id
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)

    return db_teacher


@router.get("/", response_model=Page[TeacherResponse])
def list_teachers(
    search: Optional[str] = None,
    status: Optional[bool] = None,
    tipo: Optional[TipoTeacher] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    ordenar_por: Optional[str] = "data_ativacao",
    ordem: Optional[str] = "desc",
    page: int = 1,
    limit: int = 10,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    query = db.query(Teacher).filter(
        Teacher.usuario_id == usuario.id
    )

    #  SEARCH
    if search:
        query = query.filter(
            (Teacher.name.contains(search)) |
            (Teacher.cpf.contains(search)) |
            (Teacher.funcao.contains(search))
        )

    #  STATUS
    if status is not None:
        query = query.filter(Teacher.status == status)

    #  TIPO (ENUM)
    if tipo:
        if tipo == TipoTeacher.temporario:
            query = query.filter(Teacher.temporary == True)

        elif tipo == TipoTeacher.terceirizado:
            query = query.filter(Teacher.outsource == True)

        elif tipo == TipoTeacher.concursado:
            query = query.filter(
                Teacher.temporary == False,
                Teacher.outsource == False
            )

    #  FILTRO POR DATA
    if data_inicio:
        query = query.filter(Teacher.data_ativacao >= data_inicio)

    if data_fim:
        query = query.filter(Teacher.data_ativacao <= data_fim)

    #  ORDENAÇÃO
    if ordenar_por:
        colunas_permitidas = {
            "name": Teacher.name,
            "data_ativacao": Teacher.data_ativacao,
            "status": Teacher.status
        }

        coluna = colunas_permitidas.get(ordenar_por)

        if coluna:
            if ordem == "asc":
                query = query.order_by(asc(coluna))
            else:
                query = query.order_by(desc(coluna))

    #  PAGINAÇÃO
    return paginate(query, page, limit)

@router.get("/{id}", response_model=TeacherResponse)
def get_teacher(
    id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == id,
        Teacher.usuario_id == usuario.id
    ).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    return teacher


@router.delete("/{id}")
def delete_teacher(
    id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    teacher = db.query(Teacher).filter(
        Teacher.id == id,
        Teacher.usuario_id == usuario.id
    ).first()

    if not teacher:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    db.delete(teacher)
    db.commit()

    return {"message": "Professor deletado"}
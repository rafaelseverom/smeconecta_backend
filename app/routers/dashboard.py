from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.projeto import Projeto
from app.models.teacher import Teacher
from app.models.usuario import Usuario
from app.core.security import get_usuario_logado
from app.core.enums import StatusProjeto

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/")
def dashboard(
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    total_projetos = db.query(func.count(Projeto.id)).filter(
        Projeto.usuario_id == usuario.id
    ).scalar()

    total_teachers = db.query(func.count(Teacher.id)).filter(
        Teacher.usuario_id == usuario.id
    ).scalar()

    projetos_ativos = db.query(func.count(Projeto.id)).filter(
        Projeto.usuario_id == usuario.id,
        Projeto.status == StatusProjeto.ativo
    ).scalar()

    projetos_concluidos = db.query(func.count(Projeto.id)).filter(
        Projeto.usuario_id == usuario.id,
        Projeto.status == StatusProjeto.concluido
    ).scalar()

    return {
        "total_projetos": total_projetos,
        "total_teachers": total_teachers,
        "projetos_ativos": projetos_ativos,
        "projetos_concluidos": projetos_concluidos
    }
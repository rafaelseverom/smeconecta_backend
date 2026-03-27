# ATUALIZAR ARQUIVO DE ROTAS
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.database import SessionLocal
from app.models.projeto import Projeto
from app.models.usuario import Usuario
from app.models.teacher import Teacher
from app.schemas.projeto import ProjetoCreate, ProjetoUpdate, ProjetoOut
from app.core.security import get_usuario_logado
from app.core.enums import StatusProjeto
from typing import Optional
from app.utils.pagination import paginate
from app.schemas.pagination import Page
from app.services.log_service import criar_log

router = APIRouter(prefix="/projetos", tags=["Projetos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def criar_projeto(
    dados: ProjetoCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    teachers = db.query(Teacher).filter(
        Teacher.id.in_(dados.teacher_ids)
    ).all()

    if len(teachers) != len(dados.teacher_ids):
        raise HTTPException(
            status_code=400,
            detail="Um ou mais teachers não existem"
        )

    for t in teachers:
        if t.usuario_id != usuario.id:
            raise HTTPException(
                status_code=403,
                detail="Teacher não pertence ao usuário"
            )

    if len(teachers) > 5:
        raise HTTPException(
            status_code=400,
            detail="Máximo de 5 professores por projeto"
        )

    novo_projeto = Projeto(
        nome=dados.nome,
        descricao=dados.descricao,
        usuario_id=usuario.id
    )

    novo_projeto.teachers = teachers

    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)

    criar_log(
    db,
    usuario.id,
    "CRIAR_PROJETO",
    f"Projeto {novo_projeto.id} criado"
)

    return novo_projeto


@router.get("/", response_model=Page[ProjetoOut])
def listar_projetos(
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    ordem: str = Query("desc"),
    status: Optional[StatusProjeto] = Query(None),
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    query = db.query(Projeto).filter(
        Projeto.usuario_id == usuario.id
    )

    if status:
        query = query.filter(Projeto.status == status)

    if ordem == "desc":
        query = query.order_by(desc(Projeto.data_criacao))
    else:
        query = query.order_by(asc(Projeto.data_criacao))

    return paginate(query, pagina, limite)


@router.get("/{projeto_id}", response_model=ProjetoOut)
def obter_projeto(
    projeto_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(
        Projeto.id == projeto_id
    ).first()

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    if projeto.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return projeto


@router.put("/{projeto_id}", response_model=ProjetoOut)
def atualizar_projeto(
    projeto_id: int,
    dados: ProjetoCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto_db = db.query(Projeto).filter(Projeto.id == projeto_id).first()

    if not projeto_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    if projeto_db.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # atualizar dados básicos
    projeto_db.nome = dados.nome
    projeto_db.descricao = dados.descricao
    projeto_db.status = dados.status

    # buscar teachers
    teachers = db.query(Teacher).filter(
        Teacher.id.in_(dados.teacher_ids)
    ).all()

    # valida existência
    if len(teachers) != len(dados.teacher_ids):
        raise HTTPException(
            status_code=400,
            detail="Um ou mais teachers não existem"
        )

    # valida dono
    for t in teachers:
        if t.usuario_id != usuario.id:
            raise HTTPException(
                status_code=403,
                detail="Teacher não pertence ao usuário"
            )

    # limite de 5
    if len(teachers) > 5:
        raise HTTPException(
            status_code=400,
            detail="Máximo de 5 professores por projeto"
        )

    # substitui relacionamento
    projeto_db.teachers = teachers

    db.commit()
    db.refresh(projeto_db)

    return projeto_db

@router.delete("/{projeto_id}")
def deletar_projeto(
    projeto_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto_db = db.query(Projeto).filter(Projeto.id == projeto_id).first()

    if not projeto_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    if projeto_db.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    db.delete(projeto_db)
    db.commit()

    criar_log(
    db,
    usuario.id,
    "DELETAR_PROJETO",
    f"Projeto {projeto_id} deletado"
)

    return {"message": "Projeto deletado com sucesso"}


@router.get("/debug/banco")
def ver_banco(
    db: Session = Depends(get_db)
):
    projetos = db.query(Projeto).all()
    return projetos

@router.post("/{projeto_id}/teachers/{teacher_id}")
def adicionar_teacher(
    projeto_id: int,
    teacher_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not projeto or not teacher:
        raise HTTPException(status_code=404, detail="Projeto ou teacher não encontrado")

    if projeto.usuario_id != usuario.id or teacher.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    if teacher in projeto.teachers:
        raise HTTPException(status_code=400, detail="Teacher já está no projeto")

    if len(projeto.teachers) >= 5:
        raise HTTPException(status_code=400, detail="Máximo de 5 professores por projeto")

    projeto.teachers.append(teacher)

    db.commit()
    return {"message": "Teacher adicionado ao projeto"}

@router.delete("/{projeto_id}/teachers/{teacher_id}")
def remover_teacher(
    projeto_id: int,
    teacher_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not projeto or not teacher:
        raise HTTPException(status_code=404, detail="Projeto ou teacher não encontrado")

    if projeto.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    if teacher not in projeto.teachers:
        raise HTTPException(status_code=400, detail="Teacher não está no projeto")

    projeto.teachers.remove(teacher)

    db.commit()
    return {"message": "Teacher removido do projeto"}
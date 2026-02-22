# ATUALIZAR ARQUIVO DE ROTAS
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.database import SessionLocal
from app.models.projeto import Projeto
from app.models.usuario import Usuario
from app.schemas.projeto import ProjetoCreate, ProjetoUpdate, ProjetoOut
from app.core.security import get_usuario_logado
from app.core.enums import StatusProjeto
from typing import Optional




router = APIRouter(prefix="/projetos", tags=["Projetos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProjetoOut)
def criar_projeto(
    projeto: ProjetoCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    novo_projeto = Projeto(
        nome=projeto.nome,
        descricao=projeto.descricao,
        status=projeto.status,
        usuario_id=usuario.id
    )

    db.add(novo_projeto)
    db.commit()
    db.refresh(novo_projeto)
    return novo_projeto

@router.get("/")
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

    # FILTRO POR STATUS
    if status:
        query = query.filter(Projeto.status == status)

    # ORDENAÇÃO
    if ordem == "desc":
        query = query.order_by(desc(Projeto.data_criacao))
    else:
        query = query.order_by(asc(Projeto.data_criacao))

    # PAGINAÇÃO
    offset = (pagina - 1) * limite
    projetos = query.offset(offset).limit(limite).all()

    return projetos



@router.get("/{projeto_id}", response_model=ProjetoOut)
def obter_projeto(
    projeto_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(Projeto.id == projeto_id).first()

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    # segurança → só dono pode ver
    if projeto.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return projeto



@router.put("/{projeto_id}", response_model=ProjetoOut)
def atualizar_projeto(
    projeto_id: int,
    projeto: ProjetoCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto_db = db.query(Projeto).filter(Projeto.id == projeto_id).first()

    if not projeto_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    #  VERIFICAÇÃO DE DONO
    if projeto_db.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    projeto_db.nome = projeto.nome
    projeto_db.descricao = projeto.descricao
    projeto_db.status = projeto.status

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

    #  VERIFICAÇÃO DE DONO
    if projeto_db.usuario_id != usuario.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    db.delete(projeto_db)
    db.commit()
    return {"message": "Projeto deletado com sucesso"}

@router.get("/debug/banco")
def ver_banco(
    db: Session = Depends(get_db)
):
    projetos = db.query(Projeto).all()
    return projetos


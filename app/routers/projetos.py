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
    # cria um novo projeto vinculado ao usuário autenticado
    novo = Projeto(
        nome=projeto.nome,
        descricao=projeto.descricao,
        status=projeto.status,
        usuario_id=usuario.id
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

@router.get("/", response_model=list[ProjetoOut])
def listar_projetos(
    pagina: int = Query(1, ge=1),
    limite: int = Query(10, ge=1, le=100),
    ordem: str = Query("desc"),
    status: Optional[StatusProjeto] = Query(None),
    nome: Optional[str] = Query(None),

    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    query = db.query(Projeto).filter(
        Projeto.usuario_id == usuario.id
    )

    # filtro status
    if status:
        query = query.filter(Projeto.status == status)

    # busca por nome
    if nome:
        query = query.filter(Projeto.nome.ilike(f"%{nome}%"))

    # ordenação
    if ordem == "desc":
        query = query.order_by(desc(Projeto.data_criacao))
    else:
        query = query.order_by(asc(Projeto.data_criacao))

    # paginação
    offset = (pagina - 1) * limite
    projetos = query.offset(offset).limit(limite).all()

    return projetos


@router.get("/{projeto_id}", response_model=ProjetoOut)
def obter_projeto(
    projeto_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(
        Projeto.id == projeto_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    return projeto



@router.put("/{projeto_id}", response_model=ProjetoOut)
def atualizar_projeto(
    projeto_id: int,
    dados: ProjetoCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(
        Projeto.id == projeto_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    projeto.nome = dados.nome
    projeto.descricao = dados.descricao
    projeto.status = dados.status

    db.commit()
    db.refresh(projeto)

    return projeto

@router.delete("/{projeto_id}")
def deletar_projeto(
    projeto_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto = db.query(Projeto).filter(
        Projeto.id == projeto_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db.delete(projeto)
    db.commit()

    return {"message": "Projeto deletado com sucesso"}

@router.get("/debug/banco")
def ver_banco(
    db: Session = Depends(get_db)
):
    projetos = db.query(Projeto).all()
    return projetos

@router.get("/stats")
def estatisticas_projetos(
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    base_query = db.query(Projeto).filter(
        Projeto.usuario_id == usuario.id
    )

    total = base_query.count()
    ativos = base_query.filter(Projeto.status == StatusProjeto.ativo).count()
    pausados = base_query.filter(Projeto.status == StatusProjeto.pausado).count()
    concluidos = base_query.filter(Projeto.status == StatusProjeto.concluido).count()

    return {
        "total": total,
        "ativos": ativos,
        "pausados": pausados,
        "concluidos": concluidos
    }

@router.get("/debug-tabelas")
def debug_tabelas(db: Session = Depends(get_db)):
    from sqlalchemy import inspect
    inspector = inspect(db.bind)
    return inspector.get_table_names()
# ATUALIZAR ARQUIVO DE ROTAS
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.projeto import Projeto
from app.schemas.projeto import ProjetoCreate, ProjetoUpdate, ProjetoOut
from app.core.security import get_usuario_logado
from app.models.usuario import Usuario


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
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    return db.query(Projeto).filter(
    Projeto.usuario_id == usuario.id
).all()



@router.put("/{projeto_id}", response_model=ProjetoOut)
def atualizar_projeto(
    projeto_id: int,
    projeto: ProjetoUpdate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    projeto_db = db.query(Projeto).filter(
        Projeto.id == projeto_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not projeto_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

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
    projeto_db = db.query(Projeto).filter(
        Projeto.id == projeto_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not projeto_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db.delete(projeto_db)
    db.commit()
    return {"message": "Projeto deletado com sucesso"}

    db.delete(projeto_db)
    db.commit()
    return {"message": "Projeto deletado com sucesso"}

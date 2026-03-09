from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.comentario import Comentario
from app.models.tarefa import Tarefa
from app.models.projeto import Projeto
from app.models.usuario import Usuario
from app.schemas.comentario import ComentarioCreate, ComentarioOut, ComentarioUpdate
from app.core.security import get_usuario_logado

router = APIRouter(prefix="/tarefas", tags=["Comentários"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{tarefa_id}/comentarios", response_model=ComentarioOut)
def criar_comentario(
    tarefa_id: int,
    comentario: ComentarioCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    tarefa = db.query(Tarefa).join(Projeto).filter(
        Tarefa.id == tarefa_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    novo_comentario = Comentario(
        texto=comentario.texto,
        tarefa_id=tarefa_id,
        usuario_id=usuario.id
    )

    db.add(novo_comentario)
    db.commit()
    db.refresh(novo_comentario)

    return novo_comentario

@router.get("/{tarefa_id}/comentarios", response_model=list[ComentarioOut])
def listar_comentarios(
    tarefa_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    # verificar se a tarefa pertence ao usuário
    tarefa = db.query(Tarefa).join(Projeto).filter(
        Tarefa.id == tarefa_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    comentarios = db.query(Comentario).filter(
        Comentario.tarefa_id == tarefa_id
    ).all()

    return comentarios

@router.delete("/comentarios/{comentario_id}")
def deletar_comentario(
    comentario_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    comentario = db.query(Comentario).filter(
        Comentario.id == comentario_id,
        Comentario.usuario_id == usuario.id
    ).first()

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    db.delete(comentario)
    db.commit()

    return {"message": "Comentário deletado com sucesso"}

@router.put("/comentarios/{comentario_id}", response_model=ComentarioOut)
def atualizar_comentario(
    comentario_id: int,
    dados: ComentarioUpdate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    comentario = db.query(Comentario).filter(
        Comentario.id == comentario_id,
        Comentario.usuario_id == usuario.id
    ).first()

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    comentario.texto = dados.texto

    db.commit()
    db.refresh(comentario)

    return comentario
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.tarefa import Tarefa
from app.models.projeto import Projeto
from app.models.usuario import Usuario
from app.schemas.tarefa import TarefaCreate, TarefaOut
from app.core.security import get_usuario_logado

router = APIRouter(prefix="/projetos", tags=["Tarefas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{projeto_id}/tarefas", response_model=TarefaOut)
def criar_tarefa(
    projeto_id: int,
    tarefa: TarefaCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    # verifica se o projeto existe e pertence ao usuário
    projeto = db.query(Projeto).filter(
        Projeto.id == projeto_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    nova_tarefa = Tarefa(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        status=tarefa.status,
        projeto_id=projeto_id,
        usuario_id=usuario.id
    )

    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return nova_tarefa
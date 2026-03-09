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

@router.get("/{projeto_id}/tarefas", response_model=list[TarefaOut])
def listar_tarefas(
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

    tarefas = db.query(Tarefa).filter(
        Tarefa.projeto_id == projeto_id
    ).all()

    return tarefas

@router.get("/tarefas/{tarefa_id}", response_model=TarefaOut)
def obter_tarefa(
    tarefa_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    tarefa = db.query(Tarefa).join(Projeto).filter(
        Tarefa.id == tarefa_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return tarefa

@router.put("/tarefas/{tarefa_id}", response_model=TarefaOut)
def atualizar_tarefa(
    tarefa_id: int,
    dados: TarefaCreate,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    tarefa = db.query(Tarefa).join(Projeto).filter(
        Tarefa.id == tarefa_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    tarefa.titulo = dados.titulo
    tarefa.descricao = dados.descricao
    tarefa.status = dados.status

    db.commit()
    db.refresh(tarefa)

    return tarefa

@router.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(
    tarefa_id: int,
    usuario: Usuario = Depends(get_usuario_logado),
    db: Session = Depends(get_db)
):
    tarefa = db.query(Tarefa).join(Projeto).filter(
        Tarefa.id == tarefa_id,
        Projeto.usuario_id == usuario.id
    ).first()

    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(tarefa)
    db.commit()

    return {"message": "Tarefa deletada com sucesso"}
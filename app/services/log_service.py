from sqlalchemy.orm import Session
from app.models.log import Log

def criar_log(db: Session, usuario_id: int, acao: str, descricao: str = None):
    log = Log(
        usuario_id=usuario_id,
        acao=acao,
        descricao=descricao
    )
    db.add(log)
    db.commit()
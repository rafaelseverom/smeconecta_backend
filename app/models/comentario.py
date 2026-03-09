from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)

    texto = Column(String, nullable=False)

    data_criacao = Column(DateTime(timezone=True), server_default=func.now())

    tarefa_id = Column(Integer, ForeignKey("tarefas.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    tarefa = relationship("Tarefa")
    usuario = relationship("Usuario")
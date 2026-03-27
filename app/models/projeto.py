from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from app.core.enums import StatusProjeto
from datetime import datetime
from app.models.associations import projeto_teacher


class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)

    status = Column(
        Enum(StatusProjeto),
        default=StatusProjeto.ativo,
        nullable=False
    )

    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="projetos")

    # 🔗 RELACIONAMENTO N:N
    teachers = relationship(
        "Teacher",
        secondary=projeto_teacher,
        back_populates="projetos"
    )
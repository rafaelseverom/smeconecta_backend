# ESTRUTURA DE CODIGOS DENTRO DO BANCO
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Enum
from app.core.enums import StatusProjeto


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


    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="projetos")

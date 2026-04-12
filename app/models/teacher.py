from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associations import projeto_teacher


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=True)
    genero = Column(String, nullable=True)
    funcao = Column(String, nullable=True)

    temporary = Column(Boolean, default=False)
    outsource = Column(Boolean, default=False)
    status = Column(Boolean, default=True)

    data_ativacao = Column(Date, nullable=True)
    data_desativacao = Column(Date, nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # 🔗 RELACIONAMENTO N:N
    projetos = relationship(
        "Projeto",
        secondary=projeto_teacher,
        back_populates="teachers"
    )

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    acao = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    data = Column(DateTime, default=datetime.utcnow)
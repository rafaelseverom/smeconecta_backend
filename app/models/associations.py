from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

projeto_teacher = Table(
    "projeto_teacher",
    Base.metadata,
    Column("projeto_id", Integer, ForeignKey("projetos.id")),
    Column("teacher_id", Integer, ForeignKey("teachers.id"))
)
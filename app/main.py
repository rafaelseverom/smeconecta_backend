from fastapi import FastAPI
from app.routers import projetos, usuarios
from app.database import Base, engine

# Cria tabelas automaticamente (SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SMEConecta - Gestão Operacional")

app.include_router(projetos.router)
app.include_router(usuarios.router)


@app.get("/")
def root():
    return {"message": "Backend SMEConecta funcionando!"}



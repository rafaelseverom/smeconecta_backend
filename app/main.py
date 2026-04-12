from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import projetos, usuarios
from app.database import Base, engine
from app.routers import tarefa
from app.routers import comentarios
from app.routers import teacher
from app.routers import dashboard
app = FastAPI(title="SMEConecta - Gestão Operacional")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cria tabelas
Base.metadata.create_all(bind=engine)

# rotas
app.include_router(projetos.router)
app.include_router(usuarios.router)
app.include_router(tarefa.router)
app.include_router(comentarios.router)
app.include_router(teacher.router)
app.include_router(dashboard.router)
@app.get("/")
def root():
    return {"message": "Backend SMEConecta funcionando!"}

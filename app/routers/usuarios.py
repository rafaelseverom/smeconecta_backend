from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.core.security import gerar_hash_senha, verificar_senha, criar_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/usuarios", tags=["Usuários"])

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UsuarioOut)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        usuario = db.query(Usuario).filter(
            Usuario.email == form_data.username
        ).first()

        if not usuario or not verificar_senha(form_data.password, usuario.senha):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = criar_token(
            dados={"sub": usuario.email},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        import traceback
        return {"error": str(e), "trace": traceback.format_exc()}

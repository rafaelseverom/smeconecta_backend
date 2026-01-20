from datetime import datetime, timedelta
from jose import jwt
import hashlib
from app.core.config import SECRET_KEY, ALGORITHM


def gerar_hash_senha(senha: str) -> str:
    """Gera hash simples para a senha usando SHA-256.

    Nota: uso de SHA-256 é suficiente para teste/local. Para produção,
    prefira um algoritmo com salt e work factor (ex: bcrypt / passlib).
    """
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def verificar_senha(senha_plana: str, hash_senha: str) -> bool:
    return gerar_hash_senha(senha_plana) == hash_senha


def criar_token(dados: dict, expires_delta: timedelta | None = None):
    to_encode = dados.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.database import SessionLocal
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def get_usuario_logado(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    db.close()

    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return usuario

import sys
import os

# garantir que o diretório do projeto esteja no import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

user_data = {"email": "teste@email.com", "senha": "123456"}

resp_create = client.post("/usuarios/", json=user_data)
print('create status', resp_create.status_code)
print('create json', resp_create.json())

login = client.post(
    "/usuarios/login",
    data={"username": user_data["email"], "password": user_data["senha"]}
)
print('login status', login.status_code)
print('login json', login.json())

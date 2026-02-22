from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_fluxo_completo_projeto():

    # ---------- CRIAR USUÁRIO ----------
    user_data = {
        "nome": "Teste User",
        "email": "teste@email.com",
        "senha": "123456"
    }

    client.post("/usuarios/", json=user_data)


    # ---------- LOGIN ----------
    login = client.post(
        "/usuarios/login",
        data={
            "username": user_data["email"],
            "password": user_data["senha"]
        }
    )

    assert login.status_code == 200

    token = login.json()["access_token"]


    # ---------- CRIAR PROJETO ----------
    projeto = {
        "nome": "Projeto Teste",
        "descricao": "Descrição teste",
        "status": "ativo"
    }

    criar = client.post(
        "/projetos/",
        json=projeto,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert criar.status_code == 200
    body = criar.json()

    assert body["nome"] == "Projeto Teste"
    assert body["status"] == "ativo"


    # ---------- LISTAR PROJETOS ----------
    lista = client.get(
        "/projetos/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert lista.status_code == 200
    assert len(lista.json()) >= 1
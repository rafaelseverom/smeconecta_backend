Alembic migration guide

Passos recomendados para sincronizar banco e migrar sem perda de dados:

1) Instale dependências (venv ativo):

```powershell
pip install -r requirements.txt
```

2) Para marcar o DB atual como já migrado (evita recriar tabelas existentes):

```powershell
# marca a versão atual (head) sem aplicar migrations
alembic stamp head
```

3) Para gerar uma migration automática (opcional):

```powershell
alembic revision --autogenerate -m "mensagem"
```

4) Para aplicar migrations:

```powershell
alembic upgrade head
```

Notas:
- O repositório já contém um arquivo inicial em `alembic/versions/0001_initial.py` que cria as tabelas `usuarios` e `projetos`.
- Se seu banco já tem essas tabelas e dados, use `alembic stamp head` antes de `alembic upgrade head` para evitar conflitos.
- Se quiser, eu executo `alembic stamp head` para você, porém isso requer que o pacote `alembic` esteja instalado no seu venv e que o comando seja executado no seu ambiente (posso gerar o comando, você executa).
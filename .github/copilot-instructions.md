# Copilot / Agente — Instruções do repositório (SMEConecta Backend)

Objetivo: orientar agentes IA que ajudam a manter/alterar este backend para priorizarem o modelo solicitado (preferência humana) e para trabalharem com segurança e consistência na base de código.

**Preferência de modelo**
- Priorizar `Claude Haiku 4.5` para geração e revisão de código neste repositório. Se não estiver disponível, usar o fallback da organização.

**Visão geral da arquitetura**
- **App principal**: `app/main.py` — FastAPI, registro de routers via `app.include_router(...)`.
- **Banco de dados**: `app/database.py` — SQLAlchemy com `engine`, `SessionLocal` e `Base`. A URL atual é `sqlite:///./smeconecta.db` (arquivo SQLite no root do projeto).
- **Modelos**: `app/models/*.py` — classes SQLAlchemy que herdam de `Base`. Exemplo: `app/models/projeto.py` define `class Projeto(Base)` com colunas `id`, `nome`, `descricao`, `status`.
- **Schemas**: `app/schemas/*.py` — Pydantic (converter/validar payloads); os schema correspondem aos modelos quando aplicável.
- **Routers**: `app/routers/*` — endpoints agrupados por recurso e importados em `app/main.py`.
- **Pontos de extensão**: `app/core/config.py` e `app/core/security.py` existem para configuração e helpers (atuais vazios — adicione código aqui para centralizar configuração e segurança).

**Padrões e convenções específicas do projeto**
- Sempre reutilize `SessionLocal` de `app/database.py` em dependências/handlers em vez de criar novas sessions/engines.
- Modelos SQLAlchemy ficam em arquivos com nome singular (`projeto.py`), routers agrupam recursos (`routers/projetos.py`).
- Quando criar novos endpoints, registre o router em `app/main.py` com `app.include_router(<router>)`.
- Não há sistema de migrations detectável — mudanças de schema podem requerer recriação manual do DB `smeconecta.db` ou incluir instruções de migração no projeto.

**Comandos úteis (desenvolvimento local — PowerShell)**
- Ativar virtualenv (PowerShell):

```powershell
& .\venv\Scripts\Activate.ps1
```

- Instalar dependências (quando `requirements.txt` preenchido):

```powershell
pip install -r requirements.txt
```

- Rodar servidor de desenvolvimento:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Exemplos de padrões encontrados (copiar/colar)**
- Registrar router (em `app/main.py`):

```python
from fastapi import FastAPI
from app.routers import projetos
app = FastAPI(title="SMEConecta - Gestão Operacional")
app.include_router(projetos.router)
```

- Definição de modelo (em `app/models/projeto.py`):

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class Projeto(Base):
    __tablename__ = "projetos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    status = Column(String)
```

**O que checar antes de mudanças grandes**
- Existe consumo externo da API que exige versão compatível? Atualize contratos antes.
- Se alterar o modelo/DB: confirme se haverá necessidade de migrações e documente o procedimento.
- Centralize configuração nova em `app/core/config.py` e lógica de autenticação em `app/core/security.py`.

**Onde o agente deve pedir confirmação humana**
- Alterações no esquema do banco (modelos) que impactem dados existentes.
- Adição de novas dependências que alterem `requirements.txt`.
- Mudanças de contrato de API público (rotas/inputs/outputs).

**Notas operacionais**
- `requirements.txt` está presente mas vazio — verifique/adicione dependências reais quando necessário.
- Não presuma que migrations (Alembic) estejam configuradas; o repositório não contém pastas de migration detectáveis.

Se quiser que eu prefira `GPT-5 mini` em vez de `Claude Haiku 4.5`, ou adicionar instruções administrativas (passo-a-passo para habilitar modelos na console da organização), diga qual modelo priorizar e eu adapto o arquivo.

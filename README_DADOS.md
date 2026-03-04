# Informações do Banco de Dados - SMEConecta Backend

## Resumo
Sistema de gestão operacional com autenticação de usuários, gerenciamento de projetos e tarefas.

## Banco de Dados
- **Type**: SQLite 3
- **Arquivo**: `smeconecta.db`
- **Localização**: Raiz do projeto

## Tabelas Principais

### 1. **usuarios** (4 colunas)
Armazena dados dos usuários do sistema.
- `id` (PK): Identificador único
- `nome`: Nome completo do usuário
- `email`: Email único para login
- `senha`: Senha hasheada (bcrypt)

### 2. **projetos** (7 colunas)
Armazena os projetos criados pelos usuários.
- `id` (PK): Identificador único
- `nome`: Nome do projeto
- `descricao`: Descrição detalhada
- `status`: Estado do projeto (`ativo`, `pausado`, `concluido`)
- `data_criacao`: Timestamp de criação
- `data_atualizacao`: Timestamp da última atualização
- `usuario_id` (FK): Referência ao proprietário

### 3. **tarefas** (8 colunas)
Lista de tarefas associadas a projetos e usuários.
- `id` (PK): Identificador único
- `titulo`: Título curto da tarefa
- `descricao`: Descrição opcional
- `status`: Estado da tarefa (`pendente`, `em_andamento`, `concluida`)
- `data_criacao`: Timestamp de criação
- `data_atualizacao`: Timestamp da última atualização
- `projeto_id` (FK): Referência ao projeto pai
- `usuario_id` (FK): Usuário responsável/criador

### 4. **alembic_version** (1 coluna)
Tabela de controle de migrações (Alembic).
- `version_num` (PK): Versão da migração aplicada

## Relacionamentos
- **Projeto → Usuário**: Um para Muitos (1:N)
  - Um usuário pode ter vários projetos
  - Um projeto pertence a apenas um usuário
- **Projeto → Tarefas**: Um para Muitos (1:N)
  - Um projeto pode conter várias tarefas
  - Uma tarefa pertence a um único projeto
- **Tarefa → Usuário**: Muitos para Um (N:1)
  - Cada tarefa está associada ao usuário que a criou/é responsável

## Enums
- **StatusProjeto**: ativo, pausado, concluido
- **StatusTarefa**: pendente, em_andamento, concluida

## Migração Atual
- **Versão**: 0001_initial (schema inicial)
- **Data**: 04/02/2026

## Arquivos Gerados
1. **SCHEMA.md** - Visualização em Markdown das tabelas e colunas (atualize após mudanças)
2. **schema.json** - Representação JSON estruturada do esquema
3. **README_DADOS.md** - Este documento

## Como Compartilhar
Envie os seguintes arquivos para seu colega:
```
SCHEMA.md           (documentação em Markdown)
schema.json         (dados estruturados em JSON)
README_DADOS.md     (este arquivo - contexto geral)
```

## Notas
- Sem criptografia aplicada no banco (SQLite)
- Senhas são hasheadas com bcrypt antes do armazenamento
- O sistema usa autenticação JWT via FastAPI
- Cada usuário só pode ver seus próprios projetos e tarefas

---
Gerado em: 04/03/2026

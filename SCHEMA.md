# Esquema do Banco de Dados SMEConecta
**Data de Geração**: 20/02/2026 15:26:31

## Tabelas

### Tabela: `projetos`

| Coluna | Tipo | Não Nulo | Chave Primária | Valor Padrão |
|--------|------|----------|----------------|---------------|
| `id` | INTEGER | ✓ | ✓ | - |
| `nome` | VARCHAR |  |  | - |
| `descricao` | VARCHAR |  |  | - |
| `status` | TEXT |  |  | 'ativo' |
| `data_criacao` | TEXT |  |  | datetime('now') |
| `data_atualizacao` | TEXT |  |  | datetime('now') |
| `usuario_id` | INTEGER |  |  | - |

---

### Tabela: `usuarios`

| Coluna | Tipo | Não Nulo | Chave Primária | Valor Padrão |
|--------|------|----------|----------------|---------------|
| `id` | INTEGER | ✓ | ✓ | - |
| `nome` | VARCHAR | ✓ |  | - |
| `email` | VARCHAR | ✓ |  | - |
| `senha` | VARCHAR | ✓ |  | - |

---

### Tabela: `alembic_version`

| Coluna | Tipo | Não Nulo | Chave Primária | Valor Padrão |
|--------|------|----------|----------------|---------------|
| `version_num` | VARCHAR(32) | ✓ | ✓ | - |

---


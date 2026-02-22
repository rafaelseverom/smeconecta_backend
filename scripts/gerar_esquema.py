import sqlite3
import json
from datetime import datetime

def extrair_esquema_banco():
    """Extrai esquema do banco SQLite e gera documentação"""
    
    conn = sqlite3.connect('smeconecta.db')
    cursor = conn.cursor()
    
    # Obter lista de tabelas
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tabelas = [row[0] for row in cursor.fetchall()]
    
    esquema = {}
    
    for tabela in tabelas:
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = cursor.fetchall()
        
        esquema[tabela] = {
            'colunas': [
                {
                    'nome': col[1],
                    'tipo': col[2],
                    'nao_nulo': bool(col[3]),
                    'valor_padrao': col[4],
                    'chave_primaria': bool(col[5])
                }
                for col in colunas
            ]
        }
        
        # Obter chaves estrangeiras
        cursor.execute(f"PRAGMA foreign_key_list({tabela})")
        fks = cursor.fetchall()
        if fks:
            esquema[tabela]['chaves_estrangeiras'] = [
                {
                    'coluna_local': fk[3],
                    'tabela_referenciada': fk[2],
                    'coluna_referenciada': fk[4]
                }
                for fk in fks
            ]
    
    conn.close()
    return esquema

def gerar_markdown(esquema):
    """Gera documento Markdown com o esquema"""
    
    md = f"""# Esquema do Banco de Dados SMEConecta
**Data de Geração**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## Tabelas

"""
    
    for tabela, info in esquema.items():
        md += f"### Tabela: `{tabela}`\n\n"
        md += "| Coluna | Tipo | Não Nulo | Chave Primária | Valor Padrão |\n"
        md += "|--------|------|----------|----------------|---------------|\n"
        
        for col in info['colunas']:
            chave_pk = "✓" if col['chave_primaria'] else ""
            nn = "✓" if col['nao_nulo'] else ""
            padrao = col['valor_padrao'] if col['valor_padrao'] else "-"
            md += f"| `{col['nome']}` | {col['tipo']} | {nn} | {chave_pk} | {padrao} |\n"
        
        # Chaves estrangeiras
        if 'chaves_estrangeiras' in info:
            md += "\n**Chaves Estrangeiras:**\n"
            for fk in info['chaves_estrangeiras']:
                md += f"- `{fk['coluna_local']}` → `{fk['tabela_referenciada']}.{fk['coluna_referenciada']}`\n"
        
        md += "\n---\n\n"
    
    return md

def gerar_json(esquema):
    """Gera documento JSON com o esquema"""
    return json.dumps(esquema, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("Extraindo esquema do banco...")
    esquema = extrair_esquema_banco()
    
    # Gerar Markdown
    md_content = gerar_markdown(esquema)
    with open('SCHEMA.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    print("✓ Arquivo 'SCHEMA.md' gerado")
    
    # Gerar JSON
    json_content = gerar_json(esquema)
    with open('schema.json', 'w', encoding='utf-8') as f:
        f.write(json_content)
    print("✓ Arquivo 'schema.json' gerado")
    
    # Imprimir resumo
    print(f"\nTabelas encontradas: {len(esquema)}")
    for tabela in esquema.keys():
        print(f"  - {tabela} ({len(esquema[tabela]['colunas'])} colunas)")

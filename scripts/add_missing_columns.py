from app.database import engine
from sqlalchemy import text
import shutil
import os
from datetime import datetime

DB_PATH = os.path.join(os.getcwd(), 'smeconecta.db')

if not os.path.exists(DB_PATH):
    print('Arquivo de DB não encontrado:', DB_PATH)
    raise SystemExit(1)

# backup
bkp_name = f"smeconecta.db.bkp.{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
shutil.copy2(DB_PATH, bkp_name)
print('Backup criado em', bkp_name)

conn = engine.connect()
cols = conn.execute(text("PRAGMA table_info('projetos')")).fetchall()
col_names = [c[1] for c in cols]
print('Colunas atuais:', col_names)
added = []
try:
    if 'status' not in col_names:
        conn.execute(text("ALTER TABLE projetos ADD COLUMN status TEXT DEFAULT 'ativo'"))
        added.append('status')
    if 'data_criacao' not in col_names:
        conn.execute(text("ALTER TABLE projetos ADD COLUMN data_criacao TEXT DEFAULT (datetime('now'))"))
        added.append('data_criacao')
    if 'data_atualizacao' not in col_names:
        conn.execute(text("ALTER TABLE projetos ADD COLUMN data_atualizacao TEXT DEFAULT (datetime('now'))"))
        added.append('data_atualizacao')
    if 'usuario_id' not in col_names:
        conn.execute(text("ALTER TABLE projetos ADD COLUMN usuario_id INTEGER"))
        added.append('usuario_id')

    if added:
        print('Colunas adicionadas:', added)
    else:
        print('Nenhuma coluna faltante encontrada.')
finally:
    conn.close()

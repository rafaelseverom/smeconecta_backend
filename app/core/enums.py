from enum import Enum

class StatusProjeto(str, Enum):
    ativo = "ativo"
    pausado = "pausado"
    concluido = "concluido"

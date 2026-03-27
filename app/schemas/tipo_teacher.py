from enum import Enum

class TipoTeacher(str, Enum):
    temporario = "temporario"
    terceirizado = "terceirizado"
    concursado = "concursado"
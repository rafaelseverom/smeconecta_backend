from datetime import date
from app.schemas.teacherResponse import TeacherBase
from app.schemas.teacherResponse import Teacher

fake_teachers_db_base: list[TeacherBase] = [

    TeacherBase(
        id=1,
        name="Carlos Silva",
        cpf="12345678900",
        temporary=False,
        outsource=False,
        status=True,
        funcao="Professor de Matemática",
    ),

    TeacherBase(
        id=2,
        name="Mariana Souza",
        cpf="98765432100",
        temporary=False,
        outsource=False,
        funcao="Professora de História",
        status=True
    ),

    TeacherBase(
        id=3,
        name="Roberto Lima",
        cpf="11122233344",
        temporary=False,
        outsource=False,
        funcao="TI",
        status=True
    ),

    TeacherBase(
        id=4,
        name="Ana Ferreira",
        cpf="55566677788",
        temporary=False,
        outsource=False,
        funcao="Coordenadora Pedagógica",
        status=True
    ),

    TeacherBase(
        id=5,
        name="Mario Bros",
        cpf="44455566677",
        temporary=True,
        outsource=False,
        funcao="Auxiliar Administrativo",
        status=True
    ),

    TeacherBase(
        id=6,
        name="Juliana Costa",
        cpf="22233344455",
        temporary=False,
        outsource=False,
        funcao="Professora de Português",
        status=True
    ),

    TeacherBase(
        id=7,
        name="Fernando Alves",
        cpf="33344455566",
        temporary=False,
        outsource=False,
        funcao="Professor de Física",
        status=True
    ),

    TeacherBase(
        id=8,
        name="Patricia Gomes",
        cpf="44455566611",
        temporary=False,
        outsource=False,
        funcao="Professora de Biologia",
        status=True
    ),

    TeacherBase(
        id=9,
        name="Ricardo Martins",
        cpf="55566677722",
        temporary=False,
        outsource=True,
        funcao="Suporte de TI",
        status=True
    ),

    TeacherBase(
        id=10,
        name="Camila Ribeiro",
        cpf="66677788833",
        temporary=False,
        outsource=False,
        funcao="Professora de Geografia",
        status=True
    ),

    TeacherBase(
        id=11,
        name="Lucas Pereira",
        cpf="77788899944",
        temporary=False,
        outsource=False,
        funcao="Professor de Química",
        status=True
    ),

    TeacherBase(
        id=12,
        name="Renata Duarte",
        cpf="88899900055",
        temporary=False,
        outsource=False,
        funcao="Orientadora Educacional",
        status=True
    ),

    TeacherBase(
        id=13,
        name="Bruno Carvalho",
        cpf="99900011166",
        temporary=False,
        outsource=False,
        funcao="Professor de Educação Física",
        status=True
    ),

    TeacherBase(
        id=14,
        name="Tatiane Lopes",
        cpf="00011122277",
        temporary=False,
        outsource=False,
        funcao="Professora de Artes",
        status=True
    ),

    TeacherBase(
        id=15,
        name="André Batista",
        cpf="11133355577",
        temporary=False,
        outsource=True,
        funcao="Manutenção",
        status=True
    ),

    TeacherBase(
        id=16,
        name="Carla Mendes",
        cpf="22244466688",
        temporary=False,
        outsource=False,
        funcao="Professora de Inglês",
        status=True
    ),

    TeacherBase(
        id=17,
        name="Eduardo Nogueira",
        cpf="33355577799",
        temporary=False,
        outsource=False,
        funcao="Professor de Filosofia",
        status=True
    ),

    TeacherBase(
        id=18,
        name="Vanessa Teixeira",
        cpf="44466688800",
        temporary=False,
        outsource=False,
        funcao="Secretária Escolar",
        status=True
    ),

    TeacherBase(
        id=19,
        name="Paulo Henrique",
        cpf="55577799911",
        temporary=False,
        outsource=False,
        funcao="Segurança",
        status=True
    ),

    TeacherBase(
        id=20,
        name="Sandra Moraes",
        cpf="66688800022",
        temporary=False,
        outsource=False,
        funcao="Diretora",
        status=True
    ),

]

fake_teachers_db_complete: list[Teacher] = [

    Teacher(
        id=1,
        name="Carlos Silva",
        temporary=False,
        outsource=False,
        cpf="12345678900",
        telefone="51991234567",
        genero="Masculino",
        nasc=date(1985,3,12),
        qtd_filhos=2,
        funcao="Professor de Matemática",
        data_ativacao=date(2015,2,1),
    ),

    Teacher(
        id=2,
        name="Mariana Souza",
        temporary=False,
        outsource=False,
        cpf="98765432100",
        telefone="51992345678",
        genero="Feminino",
        nasc=date(1990,7,21),
        qtd_filhos=1,
        funcao="Professora de História",
        data_ativacao=date(2018,2,1),
    ),

    Teacher(
        id=3,
        name="Roberto Lima",
        temporary=False,
        outsource=False,
        cpf="11122233344",
        telefone="51993456789",
        genero="Masculino",
        nasc=date(1982,11,2),
        qtd_filhos=3,
        funcao="TI",
        data_ativacao=date(2016,5,10),
    ),

    Teacher(
        id=4,
        name="Ana Ferreira",
        temporary=False,
        outsource=False,
        cpf="55566677788",
        telefone="51994567890",
        genero="Feminino",
        nasc=date(1988,4,9),
        qtd_filhos=0,
        funcao="Coordenadora Pedagógica",
        data_ativacao=date(2017,3,1),
    ),

    Teacher(
        id=5,
        name="Mario Bros",
        temporary=True,
        outsource=False,
        cpf="44455566677",
        telefone="51995678901",
        genero="Masculino",
        nasc=date(1995,1,18),
        qtd_filhos=0,
        funcao="Auxiliar Administrativo",
        data_ativacao=date(2024,2,1),
    ),

    Teacher(
        id=6,
        name="Juliana Costa",
        temporary=False,
        outsource=False,
        cpf="22233344455",
        telefone="51996789012",
        genero="Feminino",
        nasc=date(1992,5,27),
        qtd_filhos=1,
        funcao="Professora de Português",
        data_ativacao=date(2019,2,1),
    ),

    Teacher(
        id=7,
        name="Fernando Alves",
        temporary=False,
        outsource=False,
        cpf="33344455566",
        telefone="51997890123",
        genero="Masculino",
        nasc=date(1980,6,10),
        qtd_filhos=2,
        funcao="Professor de Física",
        data_ativacao=date(2014,3,10),
    ),

    Teacher(
        id=8,
        name="Patricia Gomes",
        temporary=False,
        outsource=False,
        cpf="44455566611",
        telefone="51998901234",
        genero="Feminino",
        nasc=date(1991,9,5),
        qtd_filhos=1,
        funcao="Professora de Biologia",
        data_ativacao=date(2018,2,1),
    ),

    Teacher(
        id=9,
        name="Ricardo Martins",
        temporary=False,
        outsource=True,
        cpf="55566677722",
        telefone="51999012345",
        genero="Masculino",
        nasc=date(1984,12,19),
        qtd_filhos=2,
        funcao="Suporte de TI",
        data_ativacao=date(2022,8,15),
    ),

    Teacher(
        id=10,
        name="Camila Ribeiro",
        temporary=False,
        outsource=False,
        cpf="66677788833",
        telefone="51990123456",
        genero="Feminino",
        nasc=date(1993,2,14),
        qtd_filhos=0,
        funcao="Professora de Geografia",
        data_ativacao=date(2020,2,1),
    ),

    Teacher(
        id=11,
        name="Lucas Pereira",
        temporary=False,
        outsource=False,
        cpf="77788899944",
        telefone="51991234001",
        genero="Masculino",
        nasc=date(1987,8,23),
        qtd_filhos=1,
        funcao="Professor de Química",
        data_ativacao=date(2013,2,1),
    ),

    Teacher(
        id=12,
        name="Renata Duarte",
        temporary=False,
        outsource=False,
        cpf="88899900055",
        telefone="51992345002",
        genero="Feminino",
        nasc=date(1986,1,11),
        qtd_filhos=2,
        funcao="Orientadora Educacional",
        data_ativacao=date(2012,3,5),
    ),

    Teacher(
        id=13,
        name="Bruno Carvalho",
        temporary=False,
        outsource=False,
        cpf="99900011166",
        telefone="51993456003",
        genero="Masculino",
        nasc=date(1983,10,2),
        qtd_filhos=1,
        funcao="Professor de Educação Física",
        data_ativacao=date(2016,2,1),
    ),

    Teacher(
        id=14,
        name="Tatiane Lopes",
        temporary=False,
        outsource=False,
        cpf="00011122277",
        telefone="51994567004",
        genero="Feminino",
        nasc=date(1994,4,17),
        qtd_filhos=0,
        funcao="Professora de Artes",
        data_ativacao=date(2021,2,1),
    ),

    Teacher(
        id=15,
        name="André Batista",
        temporary=False,
        outsource=True,
        cpf="11133355577",
        telefone="51995678005",
        genero="Masculino",
        nasc=date(1979,7,30),
        qtd_filhos=3,
        funcao="Manutenção",
        data_ativacao=date(2020,6,1),
    ),

    Teacher(
        id=16,
        name="Carla Mendes",
        temporary=False,
        outsource=False,
        cpf="22244466688",
        telefone="51996789006",
        genero="Feminino",
        nasc=date(1990,3,8),
        qtd_filhos=1,
        funcao="Professora de Inglês",
        data_ativacao=date(2017,2,1),
    ),

    Teacher(
        id=17,
        name="Eduardo Nogueira",
        temporary=False,
        outsource=False,
        cpf="33355577799",
        telefone="51997890007",
        genero="Masculino",
        nasc=date(1981,5,19),
        qtd_filhos=2,
        funcao="Professor de Filosofia",
        data_ativacao=date(2011,2,1),
    ),

    Teacher(
        id=18,
        name="Vanessa Teixeira",
        temporary=False,
        outsource=False,
        cpf="44466688800",
        telefone="51998900008",
        genero="Feminino",
        nasc=date(1989,9,12),
        qtd_filhos=1,
        funcao="Secretária Escolar",
        data_ativacao=date(2014,4,1),
    ),

    Teacher(
        id=19,
        name="Paulo Henrique",
        temporary=False,
        outsource=False,
        cpf="55577799911",
        telefone="51999000009",
        genero="Masculino",
        nasc=date(1978,6,25),
        qtd_filhos=3,
        funcao="Segurança",
        data_ativacao=date(2010,5,20),
    ),

    Teacher(
        id=20,
        name="Sandra Moraes",
        temporary=False,
        outsource=False,
        cpf="66688800022",
        telefone="51990111010",
        genero="Feminino",
        nasc=date(1975,2,3),
        qtd_filhos=2,
        funcao="Diretora",
        data_ativacao=date(2008,3,1),
    ),

]


def get_teachers_from_DB():    
    return fake_teachers_db_base

def get_teacher_by_id(id: int) -> Teacher | None:
    for teacher in fake_teachers_db_complete:
        if teacher.id == id:
            return teacher
    return None
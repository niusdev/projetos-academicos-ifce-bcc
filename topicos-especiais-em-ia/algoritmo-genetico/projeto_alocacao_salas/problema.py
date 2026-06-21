# problema.py
# Define a classe Aula, a lista completa de aulas e as constantes do problema.
# Todos os outros módulos importam daqui.

class Aula:
    def __init__(self, nome, inicio, fim):
        self.nome = nome
        self.inicio = inicio
        self.fim = fim

    def get_nome(self):    return self.nome
    def get_inicio(self):  return self.inicio
    def get_fim(self):     return self.fim
    def get_duracao(self): return self.fim - self.inicio

    def __repr__(self):
        return f"{self.nome} ({self.inicio}-{self.fim})"


# Constantes 
NUM_SALAS         = 10
LIMITE_HORAS_SALA = 15

# Lista de aulas 
AULAS = [
    Aula("Ingles", 7, 8), Aula("Espanhol", 8, 9), Aula("Caligrafia", 9, 10),
    Aula("Xadrez", 10, 11), Aula("Redes Neurais", 11, 12), Aula("Piano", 12, 13),
    Aula("Projeto 1", 13, 14), Aula("Dev Web", 14, 15), Aula("Linguagem", 15, 16),
    Aula("Lógica Comp", 16, 17), Aula("Automatos", 17, 18), Aula("CANA", 18, 19),
    Aula("Arquitetura", 19, 20), Aula("Pesquisa", 20, 21), Aula("Design Web", 21, 22),

    Aula("Matematica", 7, 9), Aula("Estatistica", 9, 10), Aula("POO", 10, 11),
    Aula("Hardware", 11, 12), Aula("Sistemas", 12, 13), Aula("Circuitos", 13, 15),
    Aula("Redes", 15, 17), Aula("IA", 17, 19), Aula("BancoDados", 19, 21),
    Aula("UX Design", 21, 22),

    Aula("Fisica", 7, 9), Aula("Compiladores", 9, 11), Aula("Topicos Esp", 11, 13),
    Aula("Historia", 13, 15), Aula("Geografia", 15, 17), Aula("Sociologia", 17, 19),
    Aula("Filosofia", 19, 21), Aula("Etica", 21, 22),

    Aula("Artes", 7, 9), Aula("Literatura", 9, 11), Aula("Gramatica", 11, 14),
    Aula("Redacao", 14, 16), Aula("Programacao", 16, 18), Aula("Estrutura Dados", 18, 20),
    Aula("Mat Discreta", 20, 22),

    Aula("Calculo", 7, 10), Aula("Algebra", 10, 12), Aula("Geometria", 12, 14),
    Aula("Criptografia", 14, 17), Aula("Seguranca", 17, 19), Aula("Cloud", 19, 22),

    Aula("Direito", 7, 10), Aula("Economia", 10, 13), Aula("Administracao", 13, 16),
    Aula("Contabilidade", 16, 19), Aula("Sist Operacionais", 19, 22),

    Aula("Financas", 7, 10), Aula("Comp Grafica", 10, 13), Aula("Metodologia", 13, 16),
    Aula("Calc Numerico", 16, 19), Aula("Eng Software", 19, 22),

    Aula("Sist Distribuidos", 7, 11), Aula("TCC", 11, 15), Aula("Gerencia Proj", 15, 19),
    Aula("Teoria Comp", 19, 22),

    Aula("Grafos", 7, 11), Aula("Big Data", 11, 14), Aula("Machine Learning", 14, 18),
    Aula("Visao Comp", 18, 22),

    Aula("Realidade Virtual", 7, 10), Aula("IoT", 10, 14), Aula("Bioinformatica", 14, 18),
    Aula("Sist Embarcados", 18, 22),
]

# Índice rápido nome → objeto Aula (usado pelos outros módulos)
AULAS_POR_NOME = {a.get_nome(): a for a in AULAS}


# Funções utilitárias compartilhadas
def conflita(aula_nova: Aula, outras: list) -> bool:
    """Retorna True se aula_nova sobrepõe qualquer aula em 'outras'."""
    for a in outras:
        if not (aula_nova.get_fim() <= a.get_inicio() or
                aula_nova.get_inicio() >= a.get_fim()):
            return True
    return False


def individuo_para_grade(individuo: dict) -> list:
    """
    Converte {nome: sala_id} em list[list[Aula]].
    Aulas com sala_id = None são ignoradas.
    """
    grade = [[] for _ in range(NUM_SALAS)]
    for nome, sala_id in individuo.items():
        if sala_id is not None:
            grade[sala_id].append(AULAS_POR_NOME[nome])
    return grade


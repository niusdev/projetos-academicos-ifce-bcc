# populacao.py
# Gera a população inicial chamando criar_individuo repetidamente.

from individuo import criar_individuo

def criar_populacao(tamanho: int, lista_aulas: list) -> list:
    return [criar_individuo(lista_aulas) for _ in range(tamanho)]


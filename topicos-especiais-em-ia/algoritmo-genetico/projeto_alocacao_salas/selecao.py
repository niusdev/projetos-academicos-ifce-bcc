# selecao.py
# Implementa a seleção por torneio para escolher pais para o crossover.

import random

def selecao_torneio(populacao: list, scores: list, k: int = 3) -> dict:
    candidatos = random.sample(range(len(populacao)), k)
    vencedor   = max(candidatos, key=lambda i: scores[i])
    return populacao[vencedor]



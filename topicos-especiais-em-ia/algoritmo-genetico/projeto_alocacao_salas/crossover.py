# crossover.py
# Combina dois indivíduos pais para gerar dois filhos.
# Após a combinação, chama reparar() para corrigir possíveis inconsistências.

import random
from individuo import reparar

def crossover(pai1: dict, pai2: dict) -> tuple:
    nomes = list(pai1.keys())

    # Filho 1: cada gene vem do pai1 ou pai2 com 50% de chance
    filho1_bruto = {
        nome: (pai1[nome] if random.random() < 0.5 else pai2[nome])
        for nome in nomes
    }

    # Filho 2: sorteio independente do filho 1
    filho2_bruto = {
        nome: (pai2[nome] if random.random() < 0.5 else pai1[nome])
        for nome in nomes
    }

    return reparar(filho1_bruto), reparar(filho2_bruto)


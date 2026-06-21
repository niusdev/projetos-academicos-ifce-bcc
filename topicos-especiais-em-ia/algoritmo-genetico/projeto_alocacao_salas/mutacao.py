# mutacao.py
# Aplica mutação em um indivíduo: com baixa probabilidade,
# move uma aula para uma sala diferente.

import copy
import random
from problema import AULAS_POR_NOME, NUM_SALAS, LIMITE_HORAS_SALA, conflita

def mutacao(individuo: dict, taxa: float = 0.05) -> dict:
    # Reconstrói o estado atual para checar restrições incrementalmente
    horas_por_sala = [0] * NUM_SALAS
    aulas_por_sala = [[] for _ in range(NUM_SALAS)]

    for nome, sala_id in individuo.items():
        if sala_id is not None:
            aula = AULAS_POR_NOME[nome]
            horas_por_sala[sala_id]  += aula.get_duracao()
            aulas_por_sala[sala_id].append(aula)

    novo = copy.copy(individuo)

    for nome in list(novo.keys()):
        if random.random() >= taxa:
            continue  # este gene não sofre mutação

        aula       = AULAS_POR_NOME[nome]
        sala_atual = novo[nome]

        # Remove temporariamente da sala atual
        if sala_atual is not None:
            horas_por_sala[sala_atual]  -= aula.get_duracao()
            aulas_por_sala[sala_atual].remove(aula)

        # Tenta uma sala diferente aleatória
        candidatas = [s for s in range(NUM_SALAS) if s != sala_atual]
        random.shuffle(candidatas)

        realocada = False
        for sala_nova in candidatas:
            cabe  = horas_por_sala[sala_nova] + aula.get_duracao() <= LIMITE_HORAS_SALA
            livre = not conflita(aula, aulas_por_sala[sala_nova])
            if cabe and livre:
                novo[nome] = sala_nova
                horas_por_sala[sala_nova]  += aula.get_duracao()
                aulas_por_sala[sala_nova].append(aula)
                realocada = True
                break

        if not realocada:
            # Reverte para a sala original
            novo[nome] = sala_atual
            if sala_atual is not None:
                horas_por_sala[sala_atual]  += aula.get_duracao()
                aulas_por_sala[sala_atual].append(aula)

    return novo



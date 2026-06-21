# individuo.py
# Responsável por criar um único indivíduo (solução aleatória válida)
# e por reparar indivíduos inválidos gerados pelo crossover.

import random
from problema import (
    Aula, AULAS_POR_NOME, NUM_SALAS, LIMITE_HORAS_SALA, conflita
)

def criar_individuo(lista_aulas: list) -> dict:
    individuo       = {}
    horas_por_sala  = [0] * NUM_SALAS
    aulas_por_sala  = [[] for _ in range(NUM_SALAS)]

    ordem = lista_aulas[:]
    random.shuffle(ordem)

    for aula in ordem:
        salas = list(range(NUM_SALAS))
        random.shuffle(salas)

        alocada = False
        for sala_id in salas:
            cabe  = horas_por_sala[sala_id] + aula.get_duracao() <= LIMITE_HORAS_SALA
            livre = not conflita(aula, aulas_por_sala[sala_id])
            if cabe and livre:
                individuo[aula.get_nome()]  = sala_id
                horas_por_sala[sala_id]    += aula.get_duracao()
                aulas_por_sala[sala_id].append(aula)
                alocada = True
                break

        if not alocada:
            individuo[aula.get_nome()] = None

    return individuo

def reparar(individuo_bruto: dict) -> dict:
    individuo_novo  = {}
    horas_por_sala  = [0] * NUM_SALAS
    aulas_por_sala  = [[] for _ in range(NUM_SALAS)]

    com_sala = [(n, s) for n, s in individuo_bruto.items() if s is not None]
    sem_sala = [n      for n, s in individuo_bruto.items() if s is None]

    random.shuffle(com_sala)
    pendentes = []

    for nome, sala_id in com_sala:
        aula  = AULAS_POR_NOME[nome]
        cabe  = horas_por_sala[sala_id] + aula.get_duracao() <= LIMITE_HORAS_SALA
        livre = not conflita(aula, aulas_por_sala[sala_id])

        if cabe and livre:
            individuo_novo[nome]        = sala_id
            horas_por_sala[sala_id]    += aula.get_duracao()
            aulas_por_sala[sala_id].append(aula)
        else:
            pendentes.append(nome)

    for nome in pendentes + sem_sala:
        aula  = AULAS_POR_NOME[nome]
        salas = list(range(NUM_SALAS))
        random.shuffle(salas)
        alocada = False

        for sala_id in salas:
            cabe  = horas_por_sala[sala_id] + aula.get_duracao() <= LIMITE_HORAS_SALA
            livre = not conflita(aula, aulas_por_sala[sala_id])
            if cabe and livre:
                individuo_novo[nome]        = sala_id
                horas_por_sala[sala_id]    += aula.get_duracao()
                aulas_por_sala[sala_id].append(aula)
                alocada = True
                break

        if not alocada:
            individuo_novo[nome] = None

    return individuo_novo

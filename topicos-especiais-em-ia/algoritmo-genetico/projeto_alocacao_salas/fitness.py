# fitness.py
# Avalia a qualidade de um indivíduo atribuindo uma pontuação numérica.
# Quanto maior o score, melhor a solução.

from problema import NUM_SALAS, LIMITE_HORAS_SALA, conflita, individuo_para_grade


def fitness(individuo: dict) -> float:
    grade = individuo_para_grade(individuo)

    qtd_alocadas     = sum(1 for v in individuo.values() if v is not None)
    qtd_nao_alocadas = len(individuo) - qtd_alocadas
    horas_totais     = sum(
        sum(a.get_duracao() for a in sala) for sala in grade
    )

    conflitos        = 0
    violacoes_limite = 0

    for sala in grade:
        if sum(a.get_duracao() for a in sala) > LIMITE_HORAS_SALA:
            violacoes_limite += 1
        for i in range(len(sala)):
            for j in range(i + 1, len(sala)):
                if conflita(sala[i], [sala[j]]):
                    conflitos += 1

    return (
          qtd_alocadas     * 1_000
        + horas_totais     *   100
        - qtd_nao_alocadas * 10_000
        - conflitos        * 100_000
        - violacoes_limite *  50_000
    )


def score_otimo(lista_aulas: list) -> float:
    total_aulas = len(lista_aulas)
    total_horas = sum(a.get_duracao() for a in lista_aulas)
    return total_aulas * 1_000 + total_horas * 100


# algoritmo.py
# Loop principal do algoritmo genético.
# Orquestra população, seleção, crossover, mutação e critérios de parada.

import copy
from populacao import criar_populacao
from fitness   import fitness, score_otimo
from selecao   import selecao_torneio
from crossover import crossover
from mutacao   import mutacao


def algoritmo_genetico(
    lista_aulas:       list,
    tamanho_populacao: int   = 60,
    max_geracoes:      int   = 300,
    taxa_crossover:    float = 0.85,  # probabilidade de cruzar (vs. copiar o pai)
    taxa_mutacao:      float = 0.05,  # probabilidade de mutar por gene
    k_torneio:         int   = 3,     # tamanho do torneio na seleção
    elitismo:          int   = 2,     # nº de melhores que passam direto
    tolerancia_conv:   int   = 40,    # gerações sem melhoria → parar
    callback_geracao=None,            # função(geracao, melhor_ind, melhor_score) chamada sempre que há melhoria
) -> tuple:

    otimo = score_otimo(lista_aulas)

    # Inicialização 
    populacao = criar_populacao(tamanho_populacao, lista_aulas)
    scores    = [fitness(ind) for ind in populacao]

    melhor_idx   = max(range(len(scores)), key=lambda i: scores[i])
    melhor_ind   = copy.deepcopy(populacao[melhor_idx])
    melhor_score = scores[melhor_idx]

    historico            = [melhor_score]
    geracoes_sem_melhora = 0

    print(f"[Gen   0] Score inicial: {melhor_score:>10.0f}  (ótimo = {otimo})")

    if callback_geracao is not None:
        callback_geracao(0, melhor_ind, melhor_score)

    # Loop de gerações 
    for geracao in range(1, max_geracoes + 1):

        nova_populacao = []

        # Elitismo: os N melhores passam direto para a próxima geração
        if elitismo > 0:
            elite = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
            for idx in elite[:elitismo]:
                nova_populacao.append(copy.deepcopy(populacao[idx]))

        # Preenche o restante com filhos gerados por crossover + mutação
        import random
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, scores, k_torneio)
            pai2 = selecao_torneio(populacao, scores, k_torneio)

            if random.random() < taxa_crossover:
                filho1, filho2 = crossover(pai1, pai2)
            else:
                filho1 = copy.deepcopy(pai1)
                filho2 = copy.deepcopy(pai2)

            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)

            nova_populacao.append(filho1)
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)

        populacao = nova_populacao
        scores    = [fitness(ind) for ind in populacao]

        # Atualiza o melhor global
        gen_idx   = max(range(len(scores)), key=lambda i: scores[i])
        gen_score = scores[gen_idx]

        if gen_score > melhor_score:
            melhor_score = gen_score
            melhor_ind   = copy.deepcopy(populacao[gen_idx])
            geracoes_sem_melhora = 0
        else:
            geracoes_sem_melhora += 1

        historico.append(melhor_score)

        if callback_geracao is not None:
            callback_geracao(geracao, melhor_ind, melhor_score)

        if geracao % 10 == 0:
            nao_aloc = sum(1 for v in melhor_ind.values() if v is None)
            print(f"[Gen {geracao:>4}] Score: {melhor_score:>10.0f}  "
                  f"Não alocadas: {nao_aloc:>2}  "
                  f"Sem melhoria: {geracoes_sem_melhora}")

        # Critério 2: ótimo atingido
        if melhor_score >= otimo:
            print(f"\n✅ Score ótimo atingido na geração {geracao}!")
            break

        # Critério 3: convergência
        if geracoes_sem_melhora >= tolerancia_conv:
            print(f"\n⚠️  Convergência detectada na geração {geracao}.")
            break

    return melhor_ind, historico

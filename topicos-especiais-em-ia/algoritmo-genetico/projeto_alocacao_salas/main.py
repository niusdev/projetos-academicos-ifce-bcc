# main.py
# Ponto de entrada do programa.
# Configura os parâmetros, executa o algoritmo e salva o resultado em JSON.

import json
import random

from problema     import AULAS, AULAS_POR_NOME
from algoritmo    import algoritmo_genetico
from fitness      import fitness
from problema     import individuo_para_grade
from serializacao import gerar_cores, serializar_individuo


def main():
    ##random.seed(7)  # remova para resultados diferentes a cada execução

    print("=" * 55)
    print("  ALGORITMO GENÉTICO — Alocação de Aulas em Salas")
    print("=" * 55)
    print(f"  Aulas totais : {len(AULAS)}")
    print("=" * 55 + "\n")

    cores = gerar_cores(AULAS)

    # Captura o estado completo a cada geração de melhoria
    # Cada item do histórico guarda a grade de salas E as aulas não
    # alocadas naquele momento, para a visualização exibir as duas coisas.
    historico_estados = []

    def capturar(geracao, individuo, score):
        nao_alocadas = [
            {
                "nome":   nome,
                "inicio": AULAS_POR_NOME[nome].get_inicio(),
                "fim":    AULAS_POR_NOME[nome].get_fim(),
                "cor":    cores[nome],
            }
            for nome, sid in individuo.items() if sid is None
        ]
        historico_estados.append({
            "geracao": geracao,
            "score": score,
            "salas": serializar_individuo(individuo, cores)["salas"],
            "nao_alocadas": nao_alocadas,
        })

    # Executa o algoritmo 
    melhor, historico = algoritmo_genetico(
        lista_aulas       = AULAS,
        tamanho_populacao = 80,
        max_geracoes      = 400,
        taxa_crossover    = 0.85,
        taxa_mutacao      = 0.08,
        k_torneio         = 3,
        elitismo          = 1,
        tolerancia_conv   = 60,
        callback_geracao  = capturar,
    )

    # Relatório no terminal
    nao_alocadas = [nome for nome, sid in melhor.items() if sid is None]

    print("\n" + "=" * 55)
    print("  RESULTADO FINAL")
    print("=" * 55)
    print(f"  Score final   : {fitness(melhor):.0f}")
    print(f"  Aulas alocadas: {len(AULAS) - len(nao_alocadas)} / {len(AULAS)}")
    if nao_alocadas:
        print(f"  Não alocadas  : {nao_alocadas}")
    print()

    grade = individuo_para_grade(melhor)
    for i, sala in enumerate(grade):
        horas = sum(a.get_duracao() for a in sala)
        aulas_str = ", ".join(
            repr(a) for a in sorted(sala, key=lambda x: x.get_inicio())
        )
        print(f"  Sala {i+1:>2} ({horas:>2}h): {aulas_str}")

    # Salva JSON 
    dados = {
        "horarios": list(range(7, 22)),
        "legenda": [
            {
                "nome":   a.get_nome(),
                "inicio": a.get_inicio(),
                "fim":    a.get_fim(),
                "cor":    cores[a.get_nome()],
            }
            for a in AULAS
        ],
        "historico_scores": historico,
        "historico": historico_estados,
        "resultado": serializar_individuo(melhor, cores),
    }

    with open("resultado_genetico.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print(f"\n  Estados capturados: {len(historico_estados)}")
    print("  resultado_genetico.json gerado com sucesso!")

    #  Abre a visualização web automaticamente 
    from servidor import iniciar_visualizacao
    iniciar_visualizacao(porta=5000, arquivo="index.html")


if __name__ == "__main__":
    main()

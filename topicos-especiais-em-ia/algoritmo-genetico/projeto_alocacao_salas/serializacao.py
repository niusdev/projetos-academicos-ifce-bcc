# serializacao.py
# Converte o resultado do algoritmo para o formato JSON
# compatível com a camada de visualização.

from problema import individuo_para_grade


def gerar_cores(lista_aulas: list) -> dict:
    """
    Associa uma cor hexadecimal a cada aula.
    Retorna {nome_aula: "#rrggbb"}.
    """
    paleta = [
        "#e63946", "#f4a261", "#2a9d8f", "#457b9d", "#6a4c93",
        "#ff006e", "#8338ec", "#3a86ff", "#06d6a0", "#118ab2",
        "#ef476f", "#ffd166", "#073b4c", "#8ecae6", "#219ebc",
        "#fb8500", "#ffb703", "#90be6d", "#43aa8b", "#577590",
        "#f94144", "#f3722c", "#f8961e", "#f9844a", "#f9c74f",
        "#90be6d", "#43aa8b", "#4d908e", "#577590", "#277da1",
        "#9b5de5", "#f15bb5", "#fee440", "#00bbf9", "#00f5d4",
        "#b5179e", "#7209b7", "#560bad", "#480ca8", "#3f37c9",
        "#4895ef", "#4cc9f0", "#ff595e", "#ffca3a", "#8ac926",
        "#1982c4", "#6a4c93", "#d00000", "#ffba08", "#3f88c5",
        "#136f63", "#f94144", "#277da1", "#43aa8b", "#f3722c",
        "#8338ec", "#ff006e", "#06d6a0", "#118ab2", "#ffd166",
        "#ef476f", "#3a86ff", "#2a9d8f", "#f4a261", "#6d597a",
        "#355070", "#b56576", "#e56b6f", "#eaac8b", "#84a59d",
    ]
    return {a.get_nome(): paleta[i % len(paleta)] for i, a in enumerate(lista_aulas)}


def serializar_individuo(individuo: dict, cores: dict) -> dict:
    """
    Converte um indivíduo para o formato de salas usado na visualização:

    {
      "salas": [
        {
          "nome": "Sala 1",
          "aulas": [
            {"nome": "Ingles", "inicio": 7, "fim": 8, "cor": "#e63946"},
            ...
          ]
        },
        ...
      ]
    }
    """
    grade = individuo_para_grade(individuo)
    return {
        "salas": [
            {
                "nome": f"Sala {i + 1}",
                "aulas": sorted(
                    [
                        {
                            "nome":   a.get_nome(),
                            "inicio": a.get_inicio(),
                            "fim":    a.get_fim(),
                            "cor":    cores[a.get_nome()],
                        }
                        for a in sala
                    ],
                    key=lambda x: x["inicio"],
                ),
            }
            for i, sala in enumerate(grade)
        ]
    }

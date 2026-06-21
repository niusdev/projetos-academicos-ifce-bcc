<div align="center">

# Alocação de Aulas em Salas — Algoritmo Genético
**Python · Algoritmos Bio-inspirados · Visualização Web**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

</div>

## Sobre o Projeto

Trabalho desenvolvido para a disciplina de **Tópicos Especiais em Inteligência Artificial**, com o objetivo de resolver um problema de **alocação de aulas em salas** (timetabling) usando um **algoritmo genético baseado em população**.

O problema consiste em distribuir um conjunto de aulas — cada uma com horário de início e término fixos — entre um número limitado de salas, respeitando duas restrições:

- duas aulas com horários conflitantes nunca podem ocupar a mesma sala;
- cada sala tem um limite máximo de horas de ocupação por dia.

O algoritmo evolui uma população de soluções candidatas através de **seleção por torneio**, **crossover uniforme com reparo de conflitos** e **mutação**, até encontrar uma alocação ótima (ou até atingir um critério de parada). O projeto inclui também uma **visualização web** que reproduz a evolução do algoritmo geração a geração, mostrando a grade de horários sendo montada e as aulas que ainda não conseguiram ser alocadas em cada etapa.

**Disciplina:** Tópicos Especiais em Inteligência Artificial  
**Professor:** Francisca Raquel de Vasconcelos Silveira  
**Instituição:** IFCE

## Módulos

| Módulo               | Responsabilidade                                                |
| --------------------- | ----------------------------------------------------------------- |
| `problema.py`          | Classe `Aula`, lista de aulas e constantes do domínio              |
| `individuo.py`         | Criação de soluções aleatórias e reparo de indivíduos inválidos    |
| `populacao.py`         | Geração da população                                       |
| `fitness.py`           | Avaliação e pontuação dos indivíduos                                |
| `selecao.py`           | Seleção por torneio                                                 |
| `crossover.py`         | Cruzamento uniforme entre dois indivíduos                           |
| `mutacao.py`           | Realocação aleatória de aulas com baixa probabilidade               |
| `algoritmo.py`         | Loop principal do algoritmo genético e critérios de parada          |
| `serializacao.py`      | Conversão do resultado para o formato consumido pela visualização   |
| `main.py`              | Ponto de entrada: executa o algoritmo e abre a visualização         |

<details>
<summary>Ver critérios de parada</summary>

O algoritmo encerra a busca quando o primeiro destes três critérios é atingido:

1. **Número máximo de gerações** definido em `main.py`;
2. **Valor ótimo alcançado** — todas as aulas alocadas, sem conflitos;
3. **Convergência** — um número configurável de gerações consecutivas sem melhoria no score.
</details>

## Como Rodar

**Pré-requisitos:** Python 3.10+ instalado.

```bash
# Clone o repositório (veja a seção abaixo se quiser baixar só esta pasta)
git clone https://github.com/niusdev/projetos-academicos-ifce-bcc.git
cd projetos-academicos-ifce-bcc/topicos-especiais-em-ia/algoritmo-genetico/projeto_alocacao_salas

# Execute o algoritmo
python main.py
```

> Ao terminar, o script salva `resultado_genetico.json` e abre automaticamente a visualização em `http://localhost:8080`.

**Quer só gerar o JSON, sem abrir o navegador?** Comente as duas últimas linhas de `main.py`:
```python
# from servidor import iniciar_visualizacao
# iniciar_visualizacao(porta=8080, arquivo="index.html")
```

## Como Baixar Só Esta Pasta

Este projeto vive dentro de um repositório maior, que reúne projetos acadêmicos de várias disciplinas. Para clonar **apenas esta pasta** (sem baixar os demais projetos do repositório), use o `sparse-checkout` do Git:

```bash
# 1. Clona sem baixar os arquivos ainda
git clone --no-checkout https://github.com/niusdev/projetos-academicos-ifce-bcc.git
cd projetos-academicos-ifce-bcc

# 2. Ativa o modo sparse (cone mode = mais simples e rápido)
git sparse-checkout init --cone

# 3. Define qual pasta especificamente quer baixar
git sparse-checkout set topicos-especiais-em-ia/algoritmo-genetico/projeto_alocacao_salas

# 4. Agora sim baixa os arquivos
git checkout main
```

Depois disso, `cd topicos-especiais-em-ia/algoritmo-genetico/projeto_alocacao_salas` e siga a seção **Como Rodar** acima.

## Visualização Web

A pasta inclui uma página (`index.html` + `style.css` + `script.js`) que reproduz a evolução do algoritmo:

- **Cronograma**: grade com as 10 salas e os horários de 7h às 22h, preenchida com as aulas alocadas em cada geração.
- **Aulas não alocadas**: painel que lista, em tempo real, as aulas que aquela geração ainda não conseguiu encaixar sem conflito.
- **Legenda**: painel inferior com a cor e o horário de cada aula.
- **Botão Iniciar**: reproduz o histórico de gerações do início ao fim, destacando visualmente as aulas que mudaram de sala entre uma geração e outra.

> A visualização depende de um servidor HTTP local (por isso `main.py` sobe um automaticamente) — abrir `index.html` direto no navegador, com duplo clique, não funciona porque o `fetch()` do JSON é bloqueado em arquivos `file://`.

## Estrutura de Pastas

```
projeto_alocacao_salas/
│
├── problema.py             # Classe Aula, lista de aulas, constantes
├── individuo.py            # Criação e reparo de indivíduos
├── populacao.py            # Geração da população inicial
├── fitness.py              # Função de avaliação (score)
├── selecao.py              # Seleção por torneio
├── crossover.py            # Cruzamento entre indivíduos
├── mutacao.py              # Operador de mutação
├── algoritmo.py            # Loop principal do AG
├── serializacao.py         # Conversão para o formato de visualização
├── servidor.py             # Servidor local + abertura automática do navegador
├── main.py                 # Ponto de entrada
│
├── index.html              # Página da visualização
├── style.css                # Estilo da visualização
├── script.js                 # Lógica de animação da visualização
└── resultado_genetico.json   # Gerado ao rodar main.py
```

## Stack & Dependências

Projeto escrito em **Python puro**, sem bibliotecas externas — apenas módulos da biblioteca padrão (`copy`, `json`, `random`, `http.server`, `webbrowser`). A visualização usa **HTML, CSS e JavaScript puros**, sem frameworks ou bundlers.

## Autor

Feito por **Vinícius Gomes Damascena**

[![GitHub](https://img.shields.io/badge/GitHub-niusdev-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/niusdev/projetos-academicos-ifce-bcc)
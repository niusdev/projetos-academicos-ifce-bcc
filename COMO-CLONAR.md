# Como clonar um projeto específico

Este repositório reúne vários projetos acadêmicos organizados por disciplina. Você não precisa baixar tudo — pode clonar **só a pasta do projeto que te interessa**, usando o comando abaixo.

---

## Passo a passo

```bash
# 1. Clona o repositório sem baixar os arquivos ainda
git clone --no-checkout https://github.com/niusdev/projetos-academicos-ifce-bcc.git
cd projetos-academicos-ifce-bcc

# 2. Ativa o modo sparse (baixa só pastas específicas)
git sparse-checkout init --cone

# 3. Define qual pasta você quer baixar (troque pelo caminho do projeto desejado)
git sparse-checkout set caminho/do/projeto

# 4. Baixa os arquivos
git checkout main
```

## Exemplo prático

Pra clonar só o projeto de **Algoritmo Genético — Alocação de Salas**:

```bash
git clone --no-checkout https://github.com/niusdev/projetos-academicos-ifce-bcc.git
cd projetos-academicos-ifce-bcc
git sparse-checkout init --cone
git sparse-checkout set topicos-especiais-em-ia/algoritmo-genetico/projeto_alocacao_salas
git checkout main
```

Depois disso, só essa pasta vai aparecer na sua máquina — os outros projetos do repositório ficam de fora, mesmo existindo no GitHub.


## Quer baixar mais de um projeto depois?

Sem precisar clonar tudo de novo, é só adicionar outra pasta:

```bash
git sparse-checkout add outra-disciplina/outro-projeto
```



## Quer só rodar o código, sem se importar com Git?

Se você só quer testar o projeto e não precisa do histórico de commits, pode simplesmente clonar o repositório completo e entrar na pasta — é mais simples e funciona igual, só baixa um pouco mais de conteúdo:

```bash
git clone https://github.com/niusdev/projetos-academicos-ifce-bcc.git
cd projetos-academicos-ifce-bcc/caminho/do/projeto
```


## Quer colaborar em algum projeto comigo?

Me manda uma mensagem e eu te adiciono como colaborador no repositório. Assim você pode clonar (com qualquer um dos métodos acima), fazer alterações e enviar (`git push`) normalmente.

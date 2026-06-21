let dados = null;
let indiceAtual = 0;
let animando = false;
let gradeAnterior = null;
let naoAlocadasAnteriorNomes = new Set();

async function carregarDados() {
  const resposta = await fetch("resultado_genetico.json");
  dados = await resposta.json();

  montarTabela(dados.horarios);

  atualizarTabela(0, { primeiraRenderizacao: true });
}

function montarTabela(horarios) {
  const tabela = document.getElementById("cronograma");
  tabela.innerHTML = "";

  const thead = document.createElement("thead");
  const trHead = document.createElement("tr");

  const thSala = document.createElement("th");
  thSala.textContent = "Sala / Horário";
  trHead.appendChild(thSala);

  horarios.forEach((h) => {
    const th = document.createElement("th");
    th.textContent = `${h}h - ${h + 1}h`;
    trHead.appendChild(th);
  });

  thead.appendChild(trHead);
  tabela.appendChild(thead);

  const tbody = document.createElement("tbody");

  for (let i = 0; i < 10; i++) {
    const tr = document.createElement("tr");

    const tdSala = document.createElement("td");
    tdSala.textContent = `Sala ${i + 1}`;
    tr.appendChild(tdSala);

    horarios.forEach((hora) => {
      const td = document.createElement("td");
      td.dataset.sala = i;
      td.dataset.hora = hora;
      tr.appendChild(td);
    });

    tbody.appendChild(tr);
  }

  tabela.appendChild(tbody);
}

function gerarGrade(estado) {
  const grade = {};

  estado.salas.forEach((sala, salaIndex) => {
    sala.aulas.forEach((aula) => {
      for (let h = aula.inicio; h < aula.fim; h++) {
        grade[`${salaIndex}-${h}`] = aula;
      }
    });
  });

  return grade;
}

function atualizarTabela(indice, opcoes = {}) {
  const estado = dados.historico[indice];
  const gradeAtual = gerarGrade(estado);

  const celulas = document.querySelectorAll("#cronograma td[data-sala]");

  celulas.forEach((td) => {
    const sala = td.dataset.sala;
    const hora = td.dataset.hora;
    const chave = `${sala}-${hora}`;

    const aulaAtual = gradeAtual[chave];
    const aulaAnterior = gradeAnterior ? gradeAnterior[chave] : null;

    td.className = "";
    td.style.backgroundColor = "";
    td.textContent = "";
    td.title = "";

    if (aulaAtual) {
      td.classList.add("aula");
      td.style.backgroundColor = aulaAtual.cor;
      td.textContent = aulaAtual.nome;
      td.title = `${aulaAtual.nome} (${aulaAtual.inicio}h - ${aulaAtual.fim}h)`;
    }

    const nomeAtual = aulaAtual ? aulaAtual.nome : null;
    const nomeAnterior = aulaAnterior ? aulaAnterior.nome : null;

    if (nomeAtual !== nomeAnterior) {
      if (aulaAtual) {
        // uma aula nova apareceu nesta célula: fade-in
        td.classList.add("apareceu");
      } else {
        // a aula que estava aqui foi removida: flash antes de ficar vazia
        td.classList.add("mudou");
      }
    }
  });

  gradeAnterior = gradeAtual;

  const ehUltimaGeracao = indice === dados.historico.length - 1;

  atualizarNaoAlocadas(estado, opcoes.primeiraRenderizacao, ehUltimaGeracao);
  atualizarStatus(estado);
}

function atualizarNaoAlocadas(estado, primeiraRenderizacao, ehUltimaGeracao) {
  const container = document.getElementById("naoAlocadas");
  const contagem = document.getElementById("contagemNaoAlocadas");

  const naoAlocadas = estado.nao_alocadas || [];
  contagem.textContent = naoAlocadas.length;

  atualizarFeedbackFinal(ehUltimaGeracao, naoAlocadas.length);

  const nomesAtuais = new Set(naoAlocadas.map((a) => a.nome));

  if (primeiraRenderizacao) {
    naoAlocadasAnteriorNomes = nomesAtuais;
    renderizarPainelSemAnimacao(container, naoAlocadas);
    return;
  }

  // Aulas que estavam no painel e já não estão mais (foram alocadas): fade-out e remover
  const itensExistentes = Array.from(
    container.querySelectorAll(".nao-alocada-item")
  );

  const saindo = itensExistentes.filter(
    (item) => !nomesAtuais.has(item.dataset.nome)
  );

  saindo.forEach((item) => {
    item.classList.add("saindo");
  });

  // Aulas que entraram no painel (não estavam alocadas antes, agora estão sem alocação)
  const nomesNovosNoPainel = [...nomesAtuais].filter(
    (nome) => !naoAlocadasAnteriorNomes.has(nome)
  );

  if (saindo.length > 0) {
    // espera o fade-out terminar para remover do DOM e então inserir os novos
    setTimeout(() => {
      saindo.forEach((item) => item.remove());

      if (naoAlocadas.length === 0) {
        mostrarVazio(container);
      }

      adicionarItensComFadeIn(container, naoAlocadas, nomesNovosNoPainel);
    }, 500);
  } else {
    if (naoAlocadas.length === 0) {
      mostrarVazio(container);
    } else {
      adicionarItensComFadeIn(container, naoAlocadas, nomesNovosNoPainel);
    }
  }

  naoAlocadasAnteriorNomes = nomesAtuais;
}

function renderizarPainelSemAnimacao(container, naoAlocadas) {
  container.innerHTML = "";

  if (naoAlocadas.length === 0) {
    mostrarVazio(container);
    return;
  }

  naoAlocadas.forEach((aula) => {
    container.appendChild(criarItemNaoAlocada(aula));
  });
}

function adicionarItensComFadeIn(container, naoAlocadas, nomesNovos) {
  // remove o "vazio" se existir, antes de inserir itens
  const vazio = container.querySelector(".nao-alocadas-vazio");
  if (vazio) vazio.remove();

  naoAlocadas.forEach((aula) => {
    let item = container.querySelector(
      `.nao-alocada-item[data-nome="${cssEscapeSeguro(aula.nome)}"]`
    );

    if (!item) {
      item = criarItemNaoAlocada(aula);

      if (nomesNovos.includes(aula.nome)) {
        item.classList.add("entrando");
        container.appendChild(item);
        // força reflow e remove a classe de entrada para disparar a transição
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            item.classList.remove("entrando");
          });
        });
      } else {
        container.appendChild(item);
      }
    }
  });
}

function criarItemNaoAlocada(aula) {
  const item = document.createElement("div");
  item.className = "nao-alocada-item";
  item.dataset.nome = aula.nome;

  item.innerHTML = `
    <div class="nao-alocada-cor" style="background:${aula.cor}"></div>
    <div class="nao-alocada-texto">
      <strong>${aula.nome}</strong>
      <span>${aula.inicio}h - ${aula.fim}h</span>
    </div>
  `;

  return item;
}

function atualizarFeedbackFinal(ehUltimaGeracao, quantidadeNaoAlocadas) {
  const feedback = document.getElementById("feedbackFinal");

  if (!ehUltimaGeracao) {
    feedback.className = "feedback-final";
    feedback.textContent = "";
    return;
  }

  if (quantidadeNaoAlocadas === 0) {
    feedback.textContent = "✓ Resultado final: todas as aulas foram alocadas!";
    feedback.className = "feedback-final visivel sucesso";
  } else {
    const sufixo = quantidadeNaoAlocadas === 1 ? "aula" : "aulas";
    feedback.textContent = `⚠ Resultado final: ${quantidadeNaoAlocadas} ${sufixo} não foram alocadas`;
    feedback.className = "feedback-final visivel incompleto";
  }
}

function mostrarVazio(container) {
  if (container.querySelector(".nao-alocadas-vazio")) return;
  const vazio = document.createElement("div");
  vazio.className = "nao-alocadas-vazio";
  vazio.textContent = "✓ Todas as aulas foram alocadas sem conflitos.";
  container.appendChild(vazio);
}

function cssEscapeSeguro(texto) {
  if (window.CSS && window.CSS.escape) {
    return CSS.escape(texto);
  }
  return texto.replace(/(["\\])/g, "\\$1");
}

function atualizarStatus(estado) {
  const totalAulas = dados.legenda.length;
  const alocadas = totalAulas - (estado.nao_alocadas ? estado.nao_alocadas.length : 0);

  document.getElementById("statGeracao").textContent = estado.geracao;
  document.getElementById("statScore").textContent = estado.score.toLocaleString("pt-BR");
  document.getElementById("statAlocadas").textContent = `${alocadas} / ${totalAulas}`;
}

function esperar(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function iniciarAnimacao() {
  if (animando || !dados) return;

  const btn = document.getElementById("btnIniciar");
  animando = true;
  btn.disabled = true;

  indiceAtual = 0;
  gradeAnterior = null;
  naoAlocadasAnteriorNomes = new Set();

  atualizarTabela(indiceAtual, { primeiraRenderizacao: true });

  for (let i = 1; i < dados.historico.length; i++) {
    await esperar(1200);
    indiceAtual = i;
    atualizarTabela(indiceAtual);
  }

  animando = false;
  btn.disabled = false;
}

document
  .getElementById("btnIniciar")
  .addEventListener("click", iniciarAnimacao);

carregarDados();
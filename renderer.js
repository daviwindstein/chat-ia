function gerarSugestoes(texto) {
  const sugestoes = document.getElementById("sugestoes");

  sugestoes.innerHTML = `
    <button onclick="usarSugestao('criar script')">💻 Criar Script</button>
    <button onclick="usarSugestao('criar cidade')">🏙️ Criar Cidade</button>
    <button onclick="usarSugestao('fazer animação')">🎬 Animação</button>
  `;
}

function usarSugestao(texto) {
  document.getElementById("input").value = texto;
}

const comandosPermitidos = ["notepad", "calc"];

function executarSeguro(cmd) {
  if (!comandosPermitidos.includes(cmd)) {
    alert("Comando não permitido ⚠️");
    return;
  }

  window.api.executar(cmd);
}

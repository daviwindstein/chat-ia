let ultimaResposta = "";

function falar(texto) {
  const fala = new SpeechSynthesisUtterance(texto);
  fala.lang = "pt-BR";
  speechSynthesis.speak(fala);
}

async function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const texto = input.value;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  const resposta = await perguntarIA(texto);

  chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;

  ultimaResposta = resposta;

  falar(resposta);

  gerarSugestoes();

  input.value = "";
}

function gerarSugestoes() {
  const s = document.getElementById("sugestoes");

  s.innerHTML = `
    <button onclick="usar('criar script roblox')">🎮 Script</button>
    <button onclick="usar('criar cidade roblox')">🏙️ Cidade</button>
    <button onclick="usar('fazer animação')">🎬 Animação</button>
  `;
}

function usar(texto) {
  document.getElementById("input").value = texto;
}

function executar() {
  const cmd = prompt("Digite: bloco ou calculadora");
  window.api.executar(cmd);
}

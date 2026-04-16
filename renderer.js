let ultimaResposta = "";

function falar(texto) {
  const fala = new SpeechSynthesisUtterance(texto);

  fala.lang = "pt-BR";
  fala.rate = 1;
  fala.pitch = 1;

  speechSynthesis.speak(fala);
}

async function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const texto = input.value;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  const resposta = "Oi 😄 estou funcionando!";

  chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;

  ultimaResposta = resposta;

  falar(resposta); // 🔥 AQUI FAZ ELA FALAR

  input.value = "";
}

async function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const texto = input.value;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  const resposta = await perguntarIA(texto);

  chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;

  input.value = "";
}

async function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const texto = input.value;

  if (!texto) return;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  const resposta = await perguntarIA(texto);

  chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;

  input.value = "";
}

async function gerarImagem() {
  const prompt = document.getElementById("input").value;

  const url = await gerarImagemIA(prompt);

  document.getElementById("chat").innerHTML += `
    <p><b>Imagem:</b></p>
    <img src="${url}" width="300">
  `;
}

function gerarVideo() {
  alert("🎬 Geração de vídeo é avançada — precisa API extra (posso te ajudar depois)");
}

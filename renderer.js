function responder(msg) {
  msg = msg.toLowerCase();

  if (msg.includes("oi")) {
    return "Oi 😄 tudo bem? Eu sou sua IA gamer favorita 🎮🔥";
  }

  if (msg.includes("tudo bem")) {
    return "Tudo ótimo! Melhor agora falando contigo 😎";
  }

  if (msg.includes("script")) {
    return "Bora criar script 😈💻 me fala o que você quer!";
  }

  return "Hmm 🤔 não entendi muito bem, mas tô aqui pra ajudar! 😄";
}

function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const texto = input.value;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  const resposta = responder(texto);

  chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;

  input.value = "";
}

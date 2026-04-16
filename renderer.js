function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const msg = input.value;

  chat.innerHTML += "<p><b>Você:</b> " + msg + "</p>";

  let resposta = "😄 Oi! Não entendi muito bem, mas tô aqui!";

  if (msg.includes("oi")) {
    resposta = "Oi 😄 tudo bem?";
  }

  chat.innerHTML += "<p><b>IA:</b> " + resposta + "</p>";

  input.value = "";
}

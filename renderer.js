function addMsg(texto, tipo) {
  const chat = document.getElementById("chat");

  const div = document.createElement("div");
  div.className = "msg " + tipo;
  div.innerText = texto;

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function enviar() {
  const input = document.getElementById("input");
  const texto = input.value;

  if (!texto) return;

  addMsg(texto, "user");

  input.value = "";

  const resposta = await perguntarIA(texto);

  addMsg(resposta, "ai");
}

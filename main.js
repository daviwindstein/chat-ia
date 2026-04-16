const { ipcRenderer } = require("electron");

const input = document.getElementById("msg");
const chat = document.getElementById("chat");

async function enviar() {
  const texto = input.value;
  if (!texto) return;

  addMsg(texto, "user");
  input.value = "";

  const resposta = await ipcRenderer.invoke("ia", texto);

  addMsg(resposta, "bot");
}

function addMsg(texto, tipo) {
  const div = document.createElement("div");
  div.className = tipo;
  div.innerText = texto;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// ENTER também envia
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") enviar();
});

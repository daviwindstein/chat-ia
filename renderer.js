const chat = document.getElementById("chat");
const input = document.getElementById("input");

const btnEnviar = document.getElementById("btnEnviar");
const btnImagem = document.getElementById("btnImagem");
const btnPC = document.getElementById("btnPC");

// adicionar mensagem
function addMsg(texto, tipo) {
  const div = document.createElement("div");
  div.className = "msg " + tipo;
  div.innerText = texto;

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// enviar mensagem
function enviar() {
  const texto = input.value;
  if (!texto) return;

  addMsg(texto, "user");

  // resposta fake (garante funcionamento)
  setTimeout(() => {
    addMsg("🤖 IA: Estou funcionando! 🔥", "ai");
  }, 500);
  const resposta = await window.api.perguntarIA(texto);

  input.value = "";
}

// botões
btnEnviar.onclick = enviar;

btnImagem.onclick = () => {
  addMsg("🖼️ Gerar imagem (em breve)", "ai");
};

btnPC.onclick = () => {
  alert("💻 Função PC funcionando!");
};

// ENTER pra enviar
input.addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    enviar();
  }
});

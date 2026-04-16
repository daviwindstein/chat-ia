window.addEventListener("DOMContentLoaded", () => {

  const chat = document.getElementById("chat");
  const input = document.getElementById("input");
  const btn = document.getElementById("btnEnviar");

  if (!btn) {
    alert("❌ Botão não encontrado (id errado)");
    return;
  }

  function addMsg(texto, tipo) {
    const div = document.createElement("div");
    div.className = "msg " + tipo;
    div.innerText = texto;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  async function enviar() {
    const texto = input.value;

    if (!texto) return;

    addMsg(texto, "user");
    input.value = "";

    try {
      // 🔥 TESTE GARANTIDO (sem IA ainda)
      const resposta = "🤖 IA funcionando: " + texto;

      addMsg(resposta, "ai");

    } catch (e) {
      addMsg("Erro: " + e.message, "ai");
    }
  }

  // 🔥 BOTÃO FUNCIONANDO
  btn.addEventListener("click", enviar);

  // 🔥 ENTER FUNCIONANDO
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") enviar();
  });

});

const resposta = await window.api.perguntarIA(texto);
addMsg(resposta, "ai"); // NÃO usar "texto" aqui

async function gerarScript() {
  const prompt = document.getElementById("input").value;

  const resposta = await window.api.perguntarIA(
    "Crie um script Roblox completo em Lua: " + prompt
  );

  addMsg(resposta, "ai");

  async function gerarImagem() {
  const prompt = document.getElementById("input").value;

  const url = await window.api.imagem(prompt);

  const img = document.createElement("img");
  img.src = url;
  img.style.width = "200px";

  document.getElementById("chat").appendChild(img);
}

async function gerarScript() {
  const prompt = document.getElementById("input").value;

  const resposta = await window.api.perguntarIA(
    "Crie um script Roblox completo: " + prompt
  );

  addMsg(resposta, "ai");

  window.pc.salvar("script.lua", resposta);

  addMsg("💾 Script salvo no PC!", "ai");
}

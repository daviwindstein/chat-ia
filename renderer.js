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

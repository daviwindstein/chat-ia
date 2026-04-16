window.addEventListener("DOMContentLoaded", () => {
  
  console.log("🔧 ativando botão...");

  const btn = document.getElementById("btnEnviar");
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  if (!btn) {
    console.error("❌ botão não encontrado");
    return;
  }

  // remove eventos bugados
  const novo = btn.cloneNode(true);
  btn.parentNode.replaceChild(novo, btn);

  novo.addEventListener("click", async () => {
    console.log("✅ clique funcionando");

    const texto = input.value;
    if (!texto) return;

    // mostra usuário
    const user = document.createElement("div");
    user.innerText = "Você: " + texto;
    chat.appendChild(user);

    input.value = "";

    try {
      const resposta = await window.api.perguntarIA(texto);

      const ia = document.createElement("div");
      ia.innerText = "IA: " + resposta;
      chat.appendChild(ia);

    } catch (e) {
      const erro = document.createElement("div");
      erro.innerText = "Erro: " + e.message;
      chat.appendChild(erro);
    }
  });

  // ENTER também funciona
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") novo.click();
  });
});
window.addEventListener("DOMContentLoaded", () => {
  console.log("🔧 ativando botão...");

  const btn = document.getElementById("btnEnviar");
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  if (!btn) {
    console.error("❌ botão não encontrado");
    return;
  }

  // remove eventos bugados
  const novo = btn.cloneNode(true);
  btn.parentNode.replaceChild(novo, btn);

  novo.addEventListener("click", async () => {
    console.log("✅ clique funcionando");

    const texto = input.value;
    if (!texto) return;

    // mostra usuário
    const user = document.createElement("div");
    user.innerText = "Você: " + texto;
    chat.appendChild(user);

    input.value = "";

    try {
      const resposta = await window.api.perguntarIA(texto);

      const ia = document.createElement("div");
      ia.innerText = "IA: " + resposta;
      chat.appendChild(ia);

    } catch (e) {
      const erro = document.createElement("div");
      erro.innerText = "Erro: " + e.message;
      chat.appendChild(erro);
    }
  });

  // ENTER também funciona
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") novo.click();
  });
});

document.addEventListener("click", () => {
  console.log("CLICOU EM ALGUM LUGAR");
});


window.addEventListener("load", () => {

  const botoes = document.querySelectorAll("button");

  console.log("Botões encontrados:", botoes.length);

  botoes.forEach((btn) => {
    btn.onclick = () => {
      alert("FUNCIONOU 🔥");
    };
  });

});

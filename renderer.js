async function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  if (!input || !chat) {
    alert("Erro: input ou chat não encontrado");
    return;
  }

  const texto = input.value;

  if (!texto) return;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  try {
    const resposta = await perguntarIA(texto);

    chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;
  } catch (e) {
    chat.innerHTML += `<p>❌ Erro: ${e.message}</p>`;
  }

  input.value = "";
}

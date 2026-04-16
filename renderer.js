async function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const texto = input.value;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  const resposta = await perguntarIA(texto);

  chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;

  input.value = "";
}

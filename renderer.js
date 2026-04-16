let memoria = [];

async function enviar() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const texto = input.value;

  chat.innerHTML += `<p><b>Você:</b> ${texto}</p>`;

  memoria.push({ role: "user", content: texto });

  const resposta = await perguntarIAComMemoria();

  chat.innerHTML += `<p><b>IA:</b> ${resposta}</p>`;

  memoria.push({ role: "assistant", content: resposta });

  input.value = "";
}

async function perguntarIAComMemoria() {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer SUA_API_KEY_AQUI",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: memoria
    })
  });

  const data = await res.json();
  return data.choices[0].message.content;
}

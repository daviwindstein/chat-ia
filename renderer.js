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

async function gerarImagem() {
  const prompt = document.getElementById("input").value;

  const res = await fetch("https://api.openai.com/v1/images/generations", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      prompt: prompt,
      size: "512x512"
    })
  });

  const data = await res.json();

  addMsg("🖼️ Imagem gerada:", "ai");

  const img = document.createElement("img");
  img.src = data.data[0].url;
  img.style.width = "200px";

  document.getElementById("chat").appendChild(img);
}

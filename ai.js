const API_KEY = "COLE_SUA_API_KEY_AQUI";

async function perguntarIA(texto) {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: "Você é uma IA inteligente, responde tudo de forma simples e cria scripts quando pedirem."
        },
        {
          role: "user",
          content: texto
        }
      ]
    })
  });

  const data = await res.json();

  return data.choices[0].message.content;
}

// 🖼️ IMAGEM
async function gerarImagemIA(prompt) {
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

  return data.data[0].url;
}

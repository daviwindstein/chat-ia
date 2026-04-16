const API_KEY = "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";

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

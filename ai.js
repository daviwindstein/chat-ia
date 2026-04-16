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
          content: "Você é uma IA inteligente, responde tudo de forma simples e clara."
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

const API_KEY = "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";

async function perguntarIA(texto) {
  try {
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
            content: "Você é uma IA inteligente que cria scripts, jogos e responde tudo de forma simples."
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

  } catch (e) {
    return "❌ Erro: " + e.message;
  }
}

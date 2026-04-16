const historico = [];

ipcMain.handle("ia", async (event, texto) => {
  try {
    // guarda usuário
    historico.push({ role: "user", content: texto });

    const res = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer SUA_API_KEY`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 1,
        max_tokens: 800,
        messages: [
          {
            role: "system",
            content: `
Você é uma IA avançada estilo ChatGPT.

REGRAS:
- NUNCA repita a frase do usuário
- Sempre responda com novas palavras
- Seja útil, inteligente e amigável
- Se pedirem script, gere COMPLETO
- Explique de forma simples
`
          },
          ...historico
        ]
      })
    });

    const data = await res.json();

    console.log("IA DEBUG:", data);

    if (!data.choices) {
      return "❌ erro na IA: " + JSON.stringify(data);
    }

    const resposta = data.choices[0].message.content;

    // guarda resposta
    historico.push({ role: "assistant", content: resposta });

    // limita memória
    if (historico.length > 20) historico.shift();

    return resposta;

  } catch (e) {
    return "Erro: " + e.message;
  }
});

ipcMain.handle("ia", async (event, texto) => {
  try {

    // guarda mensagem do usuário
    historico.push({ role: "user", content: texto });

    const res = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer SUA_API_KEY`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 0.9,
        max_tokens: 800,
        messages: [
          {
            role: "system",
            content: `
Você é uma IA avançada estilo ChatGPT.

REGRAS:
- Nunca repita o usuário
- Responda de forma inteligente e natural
- Seja amigável e clara
- Ajude com scripts, jogos e dúvidas
- Explique fácil
`
          },

          // 🔥 memória entra aqui
          ...historico
        ]
      })
    });

    const data = await res.json();

    const resposta = data.choices[0].message.content;

    // guarda resposta da IA também
    historico.push({ role: "assistant", content: resposta });

    return resposta;

  } catch (e) {
    return "Erro: " + e.message;
  }
});

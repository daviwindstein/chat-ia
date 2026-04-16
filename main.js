ipcMain.handle("ia", async (event, texto) => {
  try {

    const res = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer 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`,
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
Você é uma IA inteligente e criativa.

REGRAS IMPORTANTES:
- NUNCA repita exatamente o que o usuário disse
- Sempre responda diferente
- Seja natural e amigável
- Se o usuário disser "oi", responda algo como "Oi! 😄 tudo bem?"
- Se pedirem script ou jogo, crie código completo
`
          },
          {
            role: "user",
            content: texto
          }
        ]
      })
    });

    const data = await res.json();

    console.log("RESPOSTA IA:", data);

    if (!data.choices || !data.choices[0]) {
      return "❌ erro na resposta da IA";
    }

    return data.choices[0].message.content;

  } catch (e) {
    return "Erro: " + e.message;
  }
});

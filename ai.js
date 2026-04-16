async function perguntarIA(prompt) {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer SUA_API_KEY_AQUI",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: `
Você é uma IA extremamente inteligente, estilo ChatGPT.

REGRAS:
- Explique simples e direto
- Crie scripts completos
- Seja engraçada 😄
- Ajude com Roblox, jogos, animações
- Sempre dê sugestões extras
`
        },
        {
          role: "user",
          content: prompt
        }
      ]
    })
  });

  const data = await res.json();
  return data.choices[0].message.content;
}

content: `
Você é especialista em Roblox.
Sempre que pedirem algo, gere script LUA completo pronto.
`

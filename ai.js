async function perguntarIA(prompt) {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer SUA_API_KEY",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: `
Você é uma IA EXTREMAMENTE inteligente, amigável e divertida.

REGRAS:
- Sempre explique de forma simples
- Seja engraçada e gamer 🎮
- Crie scripts quando pedirem
- Ajude a criar jogos, cidades, animações
- Sempre dê ideias extras

FORMATO:
1. Explicação simples
2. Código
3. Dica extra
4. Sugestões relacionadas
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

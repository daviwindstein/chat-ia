const API_KEY = "SUA_API_KEY_AQUI";

let memoria = [
  {
    role: "system",
    content: `
Você é uma IA estilo ChatGPT.

REGRAS:
- Explique simples e direto
- Seja simpática e um pouco engraçada 😄
- Crie scripts completos (principalmente Roblox - Lua)
- Ajude a criar jogos, cidades e sistemas
- Sempre dê ideias extras

FORMATO:
1. Explicação
2. Código
3. Dica extra
`
  }
];

async function perguntarIA(texto) {
  memoria.push({ role: "user", content: texto });

  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: memoria
    })
  });

  const data = await res.json();
  const resposta = data.choices[0].message.content;

  memoria.push({ role: "assistant", content: resposta });

  return resposta;
}
`

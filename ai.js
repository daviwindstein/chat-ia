const API_KEY = "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";

let memoria = [
  {
    role: "system",
    content: `
Você é uma IA estilo ChatGPT.

REGRAS:
- Responda qualquer coisa de forma simples
- Seja simpática e divertida 😄
- Especialista em Roblox (cria scripts LUA completos)
- Sempre explique fácil
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

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
const { ipcMain } = require("electron");

let memoria = [];

ipcMain.handle("ia", async (event, texto) => {
  try {

    // adiciona usuário
    memoria.push({ role: "user", content: texto });

    const respostaAPI = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer SUA_API_KEY`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 0.95,
        max_tokens: 800,
        messages: [
          {
            role: "system",
            content: `
Você é uma IA avançada estilo ChatGPT.

REGRAS:
- Nunca repita o que o usuário falou
- Sempre responda com suas próprias palavras
- Seja inteligente, amigável e útil
- Se pedirem script, gere COMPLETO
- Se pedirem jogo, explique + código
- Responda como humano
`
          },
          ...memoria
        ]
      })
    });

    const data = await respostaAPI.json();

    console.log("DEBUG IA:", data);

    if (!data.choices) {
      return "❌ erro: " + JSON.stringify(data);
    }

    let resposta = data.choices[0].message.content;

    // 🧠 proteção anti-eco
    if (resposta.trim().toLowerCase() === texto.trim().toLowerCase()) {
      resposta = "😄 Eu entendi o que você disse! Quer que eu te ajude com algo específico?";
    }

    // salva resposta
    memoria.push({ role: "assistant", content: resposta });

    // limita memória
    if (memoria.length > 20) memoria.shift();

    return resposta;

  } catch (e) {
    return "❌ erro: " + e.message;
  }
});

    // guarda resposta
    historico.push({ role: "assistant", content: resposta });

    // limita memória
    if (historico.length > 20) historico.shift();

    return resposta;

  } catch (e) {
    return "Erro: " + e.message;
  }
});

const { app, BrowserWindow, ipcMain } = require("electron");
const fetch = require("node-fetch");

let memoria = [];

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  win.loadFile("index.html");
}

app.whenReady().then(createWindow);

ipcMain.handle("ia", async (event, texto) => {
  try {

    memoria.push({ role: "user", content: texto });

    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer SUA_API_KEY"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        temperature: 0.9,
        messages: [
          {
            role: "system",
            content: "Você é uma IA inteligente, útil e nunca repete o usuário."
          },
          ...memoria
        ]
      })
    });

    const data = await response.json();

    let resposta = data?.choices?.[0]?.message?.content || "Erro na IA";

    memoria.push({ role: "assistant", content: resposta });

    if (memoria.length > 20) memoria.shift();

    return resposta;

  } catch (err) {
    return "Erro: " + err.message;
  }
});

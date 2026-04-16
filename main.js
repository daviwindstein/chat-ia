const { app, BrowserWindow, ipcMain } = require("electron");
const fetch = require("node-fetch");
const fs = require("fs");

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

// 🔥 IA AQUI
ipcMain.handle("ia", async (event, texto) => {

  memoria.push({ role: "user", content: texto });

  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer SUA_API_KEY"
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: "Você é uma IA útil e inteligente." },
        ...memoria
      ]
    })
  });

  const data = await res.json();
  const resposta = data?.choices?.[0]?.message?.content || "Erro IA";

  memoria.push({ role: "assistant", content: resposta });

  if (memoria.length > 20) memoria.shift();

  return resposta;
});

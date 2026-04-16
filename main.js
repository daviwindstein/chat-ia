npm install node-fetch
  const { app, BrowserWindow } = require('electron');
const path = require('path');

const { app, BrowserWindow, ipcMain } = require('electron');
const fetch = require('node-fetch');

const API_KEY = "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";

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: __dirname + "/preload.js"
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

// 🔥 IA FUNCIONANDO AQUI
ipcMain.handle("perguntarIA", async (event, texto) => {
  try {
    const res = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: texto }]
      })
    });

    const data = await res.json();

    return data.choices[0].message.content;

  } catch (e) {
    return "❌ Erro: " + e.message;
  }
});

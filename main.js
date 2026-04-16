npm init -y
npm install electron

npm install electron-builder

const { app, BrowserWindow } = require('electron');
const path = require('path');

function executar() {
  const cmd = prompt("Ex: abrir bloco");
  window.api.executarSeguro(cmd);
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1000,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

function executar() {
  const comando = prompt("Digite comando (ex: notepad):");
  window.api.executar(comando);
}

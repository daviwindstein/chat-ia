const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld("api", {
  perguntarIA: (texto) => ipcRenderer.invoke("ia", texto)
});

const { contextBridge } = require('electron');
const fs = require('fs');

contextBridge.exposeInMainWorld("pc", {
  salvar: (nome, conteudo) => {
    fs.writeFileSync(nome, conteudo);
  }
});

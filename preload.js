const fs = require('fs');
const { contextBridge } = require('electron');
const { exec } = require('child_process');

contextBridge.exposeInMainWorld("api", {
  criarArquivo: (nome, conteudo) => {
    fs.writeFileSync(nome, conteudo);
  },

  executar: (cmd) => {
    exec(cmd);
  }
});

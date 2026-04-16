const { contextBridge } = require('electron');
const { exec } = require('child_process');

const comandos = {
  "bloco": "notepad",
  "calculadora": "calc"
};

contextBridge.exposeInMainWorld("api", {
  executar: (nome) => {
    if (comandos[nome]) {
      exec(comandos[nome]);
    } else {
      alert("Comando não permitido ⚠️");
    }
  }
});

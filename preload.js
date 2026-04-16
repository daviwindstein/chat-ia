const { contextBridge } = require('electron');
const { exec } = require('child_process');

const comandosPermitidos = {
  "abrir bloco": "notepad",
  "abrir calculadora": "calc"
};

contextBridge.exposeInMainWorld("api", {
  executarSeguro: (nome) => {
    if (comandosPermitidos[nome]) {
      exec(comandosPermitidos[nome]);
    } else {
      alert("Comando bloqueado ⚠️");
    }
  }
});

const { contextBridge } = require('electron');
const { exec } = require('child_process');

contextBridge.exposeInMainWorld("api", {
  executar: (cmd) => {
    if (cmd === "bloco") exec("notepad");
  }
});

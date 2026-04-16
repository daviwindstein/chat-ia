const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld("api", {
  perguntarIA: (texto) => ipcRenderer.invoke("ia", texto)
});

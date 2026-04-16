const fs = require("fs");

function executarComando(cmd) {
  if (cmd.acao === "criar_arquivo") {
    fs.writeFileSync(cmd.nome, cmd.conteudo);
    console.log("Arquivo criado!");
  }
}

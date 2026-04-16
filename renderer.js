function criarArquivoIA() {
  const nome = prompt("Nome do arquivo:");
  const conteudo = ultimaResposta;

  window.api.criarArquivo(nome, conteudo);

  alert("Arquivo criado 💻");
}

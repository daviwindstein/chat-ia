let permissao = localStorage.getItem("permissao") || "perguntar";

function definirPermissao() {
  const escolha = prompt(
    "Permitir controle do PC?\n1 = sempre\n2 = perguntar\n3 = nunca"
  );

  if (escolha == "1") permissao = "sempre";
  if (escolha == "2") permissao = "perguntar";
  if (escolha == "3") permissao = "nunca";

  localStorage.setItem("permissao", permissao);
}

async function enviar() {
  const input = document.getElementById("input").value;

  const resposta = await perguntarIA(input);

  document.getElementById("chat").innerText = resposta;
}

function executarCodigo() {
  if (!permissao) definirPermissao();

  if (permissao === "nunca") {
    alert("Acesso bloqueado");
    return;
  }

  if (permissao === "perguntar") {
    if (!confirm("Executar no PC?")) return;
  }

  const codigo = document.getElementById("chat").innerText;

  window.api.executar(codigo);
}

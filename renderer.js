function ouvir() {
  const reconhecimento = new webkitSpeechRecognition();

  reconhecimento.lang = "pt-BR";

  reconhecimento.onresult = async function(event) {
    const texto = event.results[0][0].transcript;

    document.getElementById("input").value = texto;

    enviar();
  };

  reconhecimento.start();
}

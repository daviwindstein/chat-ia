import google.generativeai as genai
import automacao
import ferramentas

# Substitua pela sua chave do Google AI Studio
MINHA_CHAVE = "SUA_API_KEY_AQUI"

genai.configure(api_key=MINHA_CHAVE)
model = genai.GenerativeModel('gemini-pro')

def iniciar_ia():
    chat = model.start_chat(history=[])
    print("🚀 IA Gamer & Dev Online! (Digite 'sair' para fechar)")

    while True:
        pergunta = input("\nO que vamos fazer no seu PC/Jogo hoje? > ")
        
        if pergunta.lower() == 'sair':
            break

        # Refina o pedido para ser mais profissional
        prompt_especial = ferramentas.formatar_prompt_gamer(pergunta)
        
        try:
            response = chat.send_message(prompt_especial)
            print(f"\n[IA RESPONDEU]:\n{response.text}")

            # Se a IA criou um script, oferece para digitar no PC
            if "```lua" in response.text or "```python" in response.text:
                escolha = input("\nDetectei um código! Quer que eu digite ele no seu PC? (s/n): ")
                if escolha.lower() == 's':
                    # Extrai apenas o código
                    codigo_puro = response.text.split("```")[1].replace("lua", "").replace("python", "")
                    automacao.digitar_no_estudio(codigo_puro)
        
        except Exception as e:
            print(f"Erro de conexão: {e}")

if __name__ == "__main__":
    iniciar_ia()

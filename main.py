import streamlit as st
import google.generativeai as genai
import pyautogui
import time
import os

# --- Configuração da Página ---
st.set_page_config(
    page_title="Chat.IA - Versão Suprema",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Configuração da API Key (Substitua pela sua!) ---
API_KEY = "AQ.Ab8RN6ItXlslhI9nmaonzaJf0skZUb9Q4332SWi1A4RgL7uAjA" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- Estilização da Página ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; padding: 10px; }
    .stSidebar { background-color: #f0f2f6; }
    .stChatInput { border-radius: 20px; }
    .stButton { border-radius: 20px; }
    .stAlert { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- Inicialização do Estado do Chat e Histórico ---
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = model.start_chat(history=[])

# --- Barra Lateral (Histórico e Configurações) ---
with st.sidebar:
    st.title("🤖 Chat.IA - Versão Suprema")
    st.subheader("Configurações")
    if st.button("Limpar Chat Atual"):
        st.session_state.mensagens = []
        st.rerun()
    st.divider()
    st.markdown("### Salvar Conversa")
    if st.button("Salvar Histórico"):
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"chat_history_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for msg in st.session_state.mensagens:
                    f.write(f"{msg['role'].upper()}: {msg['content']}\n\n")
            st.success(f"Histórico salvo em: {filename}")
        except Exception as e:
            st.error(f"Erro ao salvar o histórico: {e}")
    st.divider()
    st.info("Esta IA controla seu PC e cria scripts de Roblox automaticamente.")

# --- Área Principal do Chat ---
st.title("Gemini 2.0 - Automação Suprema")

# Exibe as mensagens na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Área de entrada de texto (Onde você escreve)
if prompt := st.chat_input("Diga o que a IA deve fazer no seu PC ou Jogo..."):
    # Exibe sua mensagem
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # IA Pensa e Responde
    with st.chat_message("assistant"):
        with st.spinner("A Chat.IA está pensando..."):
            contexto = "Você é a Chat.IA 2.0, a melhor IA Gamer e Dev. Responda de forma clara, simples e profissional. Se o usuário pedir um script, forneça o código completo e formatado."
            response = st.session_state.chat_history.send_message(f"{contexto} {prompt}")
            st.markdown(response.text)
            
            # Salva a resposta da IA
            st.session_state.mensagens.append({"role": "assistant", "content": response.text})

    # --- Automação: Injeção de Script ---
    if "```" in response.text:
        # Botão para injetar o script
        if st.button("Injetar Script no Roblox Studio"):
            st.warning("⚠️ Mude para a janela do Roblox Studio AGORA! Você tem 5 segundos.")
            for i in range(5, 0, -1):
                st.write(f"{i}...")
                time.sleep(1)
            # Tenta pegar apenas o código de dentro dos blocos ```
            try:
                codigo = response.text.split("```")[1].replace("lua", "").replace("python", "")
                pyautogui.write(codigo, interval=0.001)
                st.success("✅ Script enviado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao injetar o script: {e}")

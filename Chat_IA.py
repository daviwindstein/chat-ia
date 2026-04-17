import streamlit as st
import google.generativeai as genai
import pyautogui
import time

# Configuração da Página (Igual ao Gemini)
st.set_page_config(page_title="Chat.IA 2.0 - Versão Suprema", layout="wide")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stSidebar { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DO CÉREBRO (API) ---
# Coloque sua chave entre as aspas
API_KEY = "SUA_API_KEY_AQUI" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# --- HISTÓRICO E MEMÓRIA ---
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = model.start_chat(history=[])

# --- BARRA LATERAL (CHATS SALVOS) ---
with st.sidebar:
    st.title("🤖 Chat.IA 2.0")
    st.subheader("Histórico de Chats")
    if st.button("Clear Chat"):
        st.session_state.mensagens = []
        st.rerun()
    st.divider()
    st.info("Esta IA controla seu PC e cria scripts de Roblox automaticamente.")

# --- ÁREA DE CHAT (INTERFACE PRINCIPAL) ---
st.title("Gemini 2.0 - Automação Suprema")

# Mostra as mensagens na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- ONDE VOCÊ ESCREVE ---
if prompt := st.chat_input("Diga o que a IA deve fazer no seu PC ou Jogo..."):
    # Mostra sua mensagem
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # IA Pensa e Responde
    with st.chat_message("assistant"):
        contexto = "Você é a Chat.IA 2.0, a melhor IA Gamer e Dev. Responda de forma clara, simples e profissional. Se o usuário pedir um script, forneça o código completo."
        response = st.session_state.chat_history.send_message(f"{contexto} {prompt}")
        st.markdown(response.text)
        
        # Salva a resposta
        st.session_state.mensagens.append({"role": "assistant", "content": response.text})

    # --- PODER SUPREMO: AUTOMAÇÃO ---
    if "```" in response.text:
        if st.button("Injetar Script no PC"):
            st.warning("⚠️ Você tem 5 segundos para abrir o Roblox Studio ou Editor!")
            time.sleep(5)
            # Limpa o texto para pegar só o código
            codigo = response.text.split("```")[1].replace("lua", "").replace("python", "")
            pyautogui.write(codigo, interval=0.001)
            st.success("✅ Script enviado com sucesso!")

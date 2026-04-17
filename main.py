import streamlit as st
import google.generativeai as genai
import pyautogui
import time

# Configuração de estilo para parecer um App profissional
st.set_page_config(page_title="Chat.IA 2.0", page_icon="🤖", layout="wide")

# CSS para deixar o visual limpo e moderno
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatMessage { background-color: #1E1E1E; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO ---
API_KEY = "SUA_API_KEY_AQUI" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- INTERFACE ---
with st.sidebar:
    st.title("🤖 Chat.IA 2.0")
    st.subheader("Versão Suprema")
    if st.button("Novo Chat"):
        st.session_state.messages = []
        st.rerun()
    st.info("Especialista em Roblox Studio e Automação de PC.")

st.title("Central de Comando AI")

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Área de Escrita (Chat Input)
if prompt := st.chat_input("Como posso te ajudar no Roblox ou no seu PC hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(f"Você é a Chat.IA, a melhor IA Gamer/Dev. {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # Se gerar código, mostra o botão de automação
        if "```" in response.text:
            if st.button("Injetar Código no PC"):
                st.warning("⚠️ Mude para o Roblox Studio! Digitando em 5s...")
                time.sleep(5)
                # Pega o código e digita
                code = response.text.split("```")[1].replace("lua", "")
                pyautogui.write(code)

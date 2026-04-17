
import streamlit as st
import google.generativeai as genai

# Configuração Visual Suprema
st.set_page_config(page_title="Chat.IA 2.0", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatMessage { background-color: #1E1E1E; border-radius: 15px; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# CONFIGURAÇÃO DA CHAVE
API_KEY = "AQ.Ab8RN6ItXlslhI9nmaonzaJf0skZUb9Q4332SWi1A4RgL7uAjA" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# BARRA LATERAL
with st.sidebar:
    st.title("🤖 Chat.IA 2.0")
    st.markdown("---")
    if st.button("Novo Chat"):
        st.session_state.messages = []
        st.rerun()
    st.info("Especialista em Roblox e Automação Gamer.")

# HISTÓRICO DE CHAT
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ÁREA DE ESCRITA
if prompt := st.chat_input("Diga o que você quer criar hoje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            instrucao = "Você é a Chat.IA 2.0, a melhor IA Gamer e Dev. Responda de forma clara e profissional."
            response = st.session_state.chat.send_message(f"{instrucao} {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

import streamlit as st
import google.generativeai as genai

# CONFIGURAÇÃO VISUAL
st.set_page_config(page_title="Chat.IA 2.0", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid #00d2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- COLOQUE SUA CHAVE AQUI ---
# Verifique se não há espaços antes ou depois da chave!
API_KEY = "SUA_NOVA_API_KEY_AQUI" 

if API_KEY == "AQ.Ab8RN6LRamKSBKHwapcDoUdAVZEoAkNH-RolKfknu2QnS6yboQ":
    st.warning("Coloque sua API Key no código dentro do GitHub!")
    st.stop()

# CONFIGURAÇÃO DA IA (COM CORREÇÃO PARA ERRO 401)
try:
    genai.configure(api_key=API_KEY)
    # O comando 'transport=rest' força o uso da API Key simples
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"Erro na configuração: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# INTERFACE
st.title("⚡ Chat.IA 2.0 - Central de Comando")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("O que vamos criar no Roblox hoje?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Consultando Matrix..."):
            try:
                # Criando o chat com a correção de transporte
                chat = model.start_chat(history=[])
                instrucao = "Você é a Chat.IA 2.0, focada em Roblox e Automação."
                response = chat.send_message(f"{instrucao} {prompt}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Se der erro 401 aqui, a chave realmente está inválida
                st.error(f"ERRO DE CHAVE: {e}")
                st.info("Dica: Tente criar uma NOVA chave no Google AI Studio e verifique se o modelo 'Gemini 1.5 Pro' está disponível para você.")

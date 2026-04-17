import streamlit as st
import google.generativeai as genai

# CONFIGURAÇÃO VISUAL GAMER
st.set_page_config(page_title="Chat.IA 2.0 | Dev & Gamer", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid #00d2ff; }
    .stButton>button { border-radius: 20px; background: #00d2ff; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- COLE SUA CHAVE ABAIXO ---
API_KEY = "COLE_AQUI_SUA_CHAVE_AIZA" 

if API_KEY == "AQ.Ab8RN6LRamKSBKHwapcDoUdAVZEoAkNH-RolKfknu2QnS6yboQ":
    st.warning("⚠️ Quase lá! Cole sua API KEY no código para começar.")
    st.stop()

# CONFIGURAÇÃO DA IA (Transport=REST ajuda a evitar o erro 401)
try:
    genai.configure(api_key=API_KEY, transport='rest')
    # Usando o modelo FLASH que é mais estável para chaves novas
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro técnico: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# INTERFACE PRINCIPAL
st.title("⚡ Chat.IA 2.0 - Central de Comando")

# Exibir conversas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Onde você escreve (Chat Input)
prompt = st.chat_input("Peça um script ou tire uma dúvida de dev...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Processando na Matrix..."):
            try:
                chat = model.start_chat(history=[])
                instrucao = "Você é a Chat.IA 2.0, a melhor IA Gamer e Dev. Responda de forma épica e clara."
                response = chat.send_message(f"{instrucao} {prompt}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro na resposta: {e}")

import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Chat.IA 2.0 | Dev & Gamer",
    page_icon="⚡",
    layout="wide"
)

# 2. DESIGN PROFISSIONAL (CSS)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.8);
        border-right: 2px solid #00d2ff;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(0, 210, 255, 0.3);
        margin-bottom: 15px;
    }
    .stChatInputContainer { padding-bottom: 20px; }
    .stButton>button {
        border-radius: 20px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SEGURANÇA DA CHAVE
# COLOQUE SUA CHAVE DENTRO DAS ASPAS ABAIXO
API_KEY = "AQ.Ab8RN6ItXlslhI9nmaonzaJf0skZUb9Q4332SWi1A4RgL7uAjA" 

if API_KEY == "SUA_API_KEY_AQUI" or not API_KEY:
    st.error("⚠️ ERRO: Adicione sua API KEY no código!")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"Erro: {e}")

# 4. MEMÓRIA
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. SIDEBAR
with st.sidebar:
    st.title("🤖 Chat.IA 2.0")
    if st.button("🗑️ Limpar Tudo"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()

# 6. EXIBIÇÃO
st.title("⚡ Central de Comando Gamer")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. INPUT (CORRIGIDO)
prompt = st.chat_input("O que vamos desenvolver hoje?")

if prompt:
    # Salva e mostra mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("🚀 Processando..."):
            try:
                instrucao = "Você é a Chat.IA 2.0, a melhor IA Gamer e Dev. Seja claro."
                response = st.session_state.chat_session.send_message(f"{instrucao} {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro: {e}")

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
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px #00d2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SEGURANÇA DA CHAVE
# SUBSTITUA ABAIXO PELA SUA CHAVE REAL
API_KEY = "SUA_CHAVE_AQUI" 

if API_KEY == "AQ.Ab8RN6ItXlslhI9nmaonzaJf0skZUb9Q4332SWi1A4RgL7uAjA" or not API_KEY:
    st.error("⚠️ ERRO: Você precisa colocar sua API KEY dentro do código no GitHub!")
    st.stop()

# Configuração do Modelo
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"Erro na configuração: {e}")

# 4. MEMÓRIA DO CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL
with st.sidebar:
    st.title("🤖 Chat.IA 2.0")
    st.markdown("**Status:** 🟢 Online")
    if st.button("🗑️ Limpar Chat"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    st.divider()
    st.info("Especialista em Roblox Studio e Automação.")

# 6. EXIBIÇÃO
st.title("⚡ Central de Comando Gamer")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. ÁREA DE ESCRITA (ONDE A MÁGICA ACONTECE)
if prompt := st.chat_input("O

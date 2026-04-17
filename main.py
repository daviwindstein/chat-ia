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
    /* Fundo e Texto */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    
    /* Personalização da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.7);
        border-right: 2px solid #00d2ff;
    }
    
    /* Bolhas do Chat */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 1px solid rgba(0, 210, 255, 0.3);
        margin-bottom: 15px;
    }

    /* Input de Texto */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #00d2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SEGURANÇA DA CHAVE (Siga as instruções abaixo!)
# DICA: No Streamlit Cloud, você pode usar st.secrets["GOOGLE_API_KEY"]
API_KEY = "AQ.Ab8RN6ItXlslhI9nmaonzaJf0skZUb9Q4332SWi1A4RgL7uAjA" 

if API_KEY == "COLE_AQUI_SUA_CHAVE_SEM_ESPAÇOS" or not API_KEY:
    st.error("⚠️ ERRO DE AUTENTICAÇÃO: Você esqueceu de colocar sua API KEY no código!")
    st.stop()

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
except Exception as e:
    st.error(f"Erro ao configurar IA: {e}")

# 4. MEMÓRIA DO CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# 5. BARRA LATERAL
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    st.title("Chat.IA 2.0")
    st.markdown("**Status:** 🟢 Online")
    st.markdown("---")
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    st.divider()
    st.info("Esta IA é especializada em criar scripts para Roblox Studio e automação gamer.")

# 6. EXIBIÇÃO DAS MENSAGENS
st.title("⚡ Central de Comando Gamer")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. ÁREA DE ESCRITA
if prompt := st.chat_input("Diga seu comando (ex: 'Crie um script de pulo duplo')..."):
    # Mostra mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("🚀 Processando dados da Matrix..."):
            try:
                instrucao = (
                    "Você é a Chat.IA 2.0, a melhor IA Gamer e Dev do mundo. "
                    "Responda de forma clara, amigável e use emojis. "
                    "Se criar scripts, explique onde colar no Roblox Studio."
                )
                response = st.session_state.chat_session.send_message(f"{instrucao} {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content

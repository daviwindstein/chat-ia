import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# 1. ESTILO VISUAL (Neon, Dark e Fácil de Usar)
st.set_page_config(page_title="Chat.IA 2.0 OMNI PRO", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #7000ff;
        box-shadow: 0px 5px 15px rgba(112, 0, 255, 0.4);
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #7000ff; }
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 55px; border: none;
    }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE E DADOS EM TEMPO REAL
GOOGLE_CHAVE = "SUA_CHAVE_AQUI"
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")
CIDADE = "Brasil" # Você pode mudar para sua cidade específica

# 3. MEMÓRIA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL
with st.sidebar:
    st.title("🔮 OMNI HUB SUPREMO")
    st.write(f"📅 **Hoje:** {AGORA}")
    
    opcoes_ia = {
        "💎 Gemini 3.1 Pro": "gemini-1.5-pro",
        "🚀 SuperGroq": "gemini-1.5-flash",
        "🤖 ChatGPT Pro": "gemini-1.5-pro",
        "🧠 Claude 3.6 Pro": "gemini-1.5-pro"
    }
    
    escolha_nome = st.selectbox("🤖 ESCOLHA SUA IA:", list(opcoes_ia.keys()))
    modelo_tecnico = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Conversas")
    for cid in list(st.session_state.historico_chats.keys()):
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:15] if conteudo else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 5. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE
st.title(f"✨ {escolha_nome}")
st.write(f"Opa! Sou sua IA assistente. Estou pronta para criar scripts de Roblox, ajudar nos estudos ou só bater um papo engraçado! 🚀")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE RESPOSTA (MUITO GENTIL E INTELIGENTE)
prompt = st.chat_input("Manda ver! O que vamos fazer hoje?")

if prompt:
    if GOOGLE_CHAVE == "AIzaSyD04qcTm5fX2ZrMvcsiFrvXUTXu4KiyO4M":
        st.error("🚨 Mano, esqueceu a chave! Coloca ela na linha 42.")
        st.stop()

    genai.configure(api_key=GOOGLE_CHAVE)
    
    # Instrução Mestra: Gentil, Engraçada, Inteligente e Sabichona
    PROMPT_MESTRE = f"""
    Você é a Chat.IA 2.0 Omni Pro. 
    Hoje é dia {AGORA} em {CIDADE}. 
    
    PERSONALIDADE: Muito gentil, engraçada (pode fazer piadas leves), inteligente e prestativa. 
    HABILIDADES: 
    1. Mestra em Roblox (Lua): Cria scripts perfeitos para RPGs, terror e sistemas.
    2. Professora nota 10: Explica lição de casa de um jeito fácil e rápido.
    3. Atualizada: Sabe que estamos em 2026.
    
    Seja amigável como um melhor amigo programador!
    """

    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔮 Consultando os astros (e o código)..."):
            try:
                model = genai.GenerativeModel(
                    model_name=modelo_tecnico,
                    system_instruction=PROMPT_MESTRE,
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                    ]
                )
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st

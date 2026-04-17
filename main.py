import streamlit as st
from groq import Groq
import uuid

# 1. ESTILO VISUAL (Preto, Roxo e Neon)
st.set_page_config(page_title="Chat.IA 2.0 Omni", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 2px solid #7000ff;
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #7000ff; }
    .stButton>button {
        width: 100%; border-radius: 8px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 45px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE MEMÓRIA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 3. CONFIGURAÇÃO DA CHAVE
CHAVE_GROQ = "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" # COLOQUE SUA KEY AQUI

if CHAVE_GROQ == "SUA_CHAVE_AQUI":
    st.error("🚨 Coloque a Chave da Groq na linha 52!")
    st.stop()

client = Groq(api_key=CHAVE_GROQ)

# 4. BARRA LATERAL (HISTÓRICO E FERRAMENTAS)
with st.sidebar:
    st.title("🌐 Chat.IA Omni")
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Chats Recentes")
    for cid in list(st.session_state.historico_chats.keys()):
        # Mostra os primeiros 15 caracteres da primeira mensagem como título
        label = st.session_state.historico_chats[cid][0]["content"][:15] if st.session_state.historico_chats[cid] else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

    st.divider()
    st.subheader("🚀 Super Poderes")
    if st.button("🖼️ Prompt de Imagem"): st.info("Descreva a cena para eu criar o prompt!")
    if st.button("📚 Ajudante Escolar"): st.success("Modo Prova & Trabalho Ativado!")
    if st.button("🎮 Roblox Script"): st.warning("Mestre em Lua Ativo!")

# 5. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE
st.title("⚡ Chat.IA 2.0 Omni-Inteligência")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA E RESPOSTA
prompt = st.chat_input("Como posso te ajudar agora?")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):

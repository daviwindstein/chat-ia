import streamlit as st
import requests
import json
import uuid

# 1. ESTILO VISUAL PREMIUM (Neon e Contraste)
st.set_page_config(page_title="Chat.IA 2.0 OMNI PRO", page_icon="🔮", layout="wide")

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
        font-size: 19px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #7000ff; }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 50px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE DO OPENROUTER (Atenção: verifique se não há espaços!)
OPENROUTER_KEY = "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"

# 3. MEMÓRIA DO SISTEMA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - SELETOR DE IAs PRO
with st.sidebar:
    st.title("🔮 OMNI PRO HUB")
    
    opcoes_ia = {
        "🚀 SuperGroq (Llama 3.3)": "meta-llama/llama-3.3-70b-instruct",
        "💎 Gemini 3.1 Pro": "google/gemini-pro-1.5",
        "🤖 ChatGPT Pro (GPT-4o)": "openai/gpt-4o",
        "🧠 Claude 3.6 Pro": "anthropic/claude-3.5-sonnet",
        "🆓 Gemini 2.0 (GRÁTIS)": "google/gemini-2.0-flash-exp:free"
    }
    
    escolha_nome = st.selectbox("ESCOLHA O CÉREBRO DA IA:", list(opcoes_ia.keys()))
    ia_modelo_real = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Histórico")
    for cid in list(st.session_state.historico_chats.keys()):
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:20] if conteudo else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 5. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE PRINCIPAL
st.title(f"⚡ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA E LÓGICA DE CHAMADA (CORRIGIDA)
prompt = st.chat_input("Pergunte qualquer coisa...")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🔧 Conectando ao {escolha_nome}..."):
            try:
                # Verificação de segurança da chave
                if OPENROUTER_KEY == "SUA_CHAVE_AQUI" or len(OPENROUTER_KEY) < 10:
                    st.error("🚨 Chave API inválida! Cole sua chave do OpenRouter na linha 48.")
                    st.stop()

                headers = {
                    "Authorization": f"Bearer {OPENROUTER_KEY.strip()}", # .strip() remove espaços extras
                    "Content-Type": "application/json",

import streamlit as st
import requests
import json
import uuid

# 1. ESTILO VISUAL (Preto Absoluto e Neon Roxo/Ciano)
st.set_page_config(page_title="Chat.IA 2.0 OMNI", page_icon="🔮", layout="wide")

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
        width: 100%; border-radius: 8px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 45px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DE CHAVES
# Coloca aqui a chave que criaste no OpenRouter
OPENROUTER_KEY = "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"

# 3. MEMÓRIA DO SISTEMA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - SELETOR DE CÉREBRO
with st.sidebar:
    st.title("🔮 OMNI HUB IA")
    
    # Lista das melhores IAs do mundo disponíveis no OpenRouter
    ia_modelo = st.selectbox(
        "ESCOLHA A IA (VERSÕES PRO):",
        [
            "openai/gpt-4o", 
            "anthropic/claude-3.5-sonnet", 
            "google/gemini-pro-1.5", 
            "meta-llama/llama-3.1-405b",
            "mistralai/mistral-large"
        ]
    )
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Conversas Guardadas")
    for cid in list(st.session_state.historico_chats.keys()):
        label = st.session_state.historico_chats[cid][0]["content"][:18] if st.session_state.historico_chats[cid] else "Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 5. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE PRINCIPAL
st.title(f"🚀 Chat.IA 2.0: {ia_modelo.split('/')[-1].upper()}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE CHAMADA VIA OPENROUTER
prompt = st.chat_input("Diz-me o que queres criar ou estudar...")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {ia_modelo} está a pensar..."):
            try:
                # Chamada para a API do OpenRouter
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_KEY}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": ia_modelo,
                        "messages": [
                            {"role": "system", "content": "És a Chat.IA 2.0 Omni. Mestra em Roblox, Escola e Automação."},
                            {"role": "user", "content": prompt}
                        ]
                    })
                )
                
                dados = response.json()
                # Extrai a resposta correta do JSON do OpenRouter
                if "choices" in dados:
                    resposta = dados["choices"][0]["message"]["content"]
                    st.write(resposta)
                    mensagens_atuais.append({"role": "assistant", "content": resposta})
                    st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                else:
                    st.error(f"Erro na API: {dados}")
                
            except Exception as e:
                st.error(f"Falha na conexão: {e}")

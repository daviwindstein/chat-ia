import streamlit as st
import requests
import json
import uuid

# 1. ESTILO VISUAL (Preto Absoluto e Neon Roxo/Ciano)
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
        width: 100%; border-radius: 8px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 50px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE DO OPENROUTER
OPENROUTER_KEY = "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"

# 3. MEMÓRIA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - SELETOR DE CÉREBRO PRO
with st.sidebar:
    st.title("🔮 OMNI PRO HUB")
    
    # Lista com os modelos PRO que você solicitou (usando IDs do OpenRouter)
    ia_modelo = st.selectbox(
        "ESCOLHA A SUA IA PRO:",
        [
            "meta-llama/llama-3.3-70b-instruct", # SuperGroq
            "google/gemini-pro-1.5",            # Gemini 3.1 Pro
            "openai/gpt-4o",                    # Chat GPT Pro
            "anthropic/claude-3.5-sonnet",      # Claude 3.6 Pro
            "openrouter/auto"                   # Automático (Melhor custo/benefício)
        ]
    )
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Histórico de Chats")
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
# Formata o nome para exibição amigável
exibir_nome = ia_modelo.split('/')[-1].replace('-', ' ').upper()
st.title(f"⚡ Chat.IA 2.0: {exibir_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA E LÓGICA
prompt = st.chat_input("Comande a sua IA Pro...")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {exibir_nome} processando..."):
            try:
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": ia_modelo,
                    "messages": [
                        {"role": "system", "content": "Você é a Chat.IA 2.0 Omni Pro. Mestra absoluta em Roblox (Lua), Escola e Automação."},
                        {"role": "user", "content": prompt}
                    ]
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )
                
                resultado = response.json()
                
                if "choices" in resultado:
                    resposta_ia = resultado["choices"][0]["message"]["content"]
                    st.write(resposta_ia)
                    mensagens_atuais.append({"role": "assistant", "content": resposta_ia})
                    st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                else:
                    st.error(f"Erro na conta OpenRouter: {resultado.get('error', {}).get('message', 'Erro desconhecido')}")
                    
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

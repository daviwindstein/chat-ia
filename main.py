import streamlit as st
import requests
import json
import uuid

# 1. ESTILO VISUAL PREMIUM
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

# 2. CHAVE DO OPENROUTER
OPENROUTER_KEY = "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"

# 3. MEMÓRIA DO SISTEMA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL
with st.sidebar:
    st.title("🔮 OMNI PRO HUB")
    
    opcoes_ia = {
        "🚀 SuperGroq": "meta-llama/llama-3.3-70b-instruct",
        "💎 Gemini 3.1 Pro": "google/gemini-pro-1.5",
        "🤖 ChatGPT Pro": "openai/gpt-4o",
        "🧠 Claude 3.6 Pro": "anthropic/claude-3.5-sonnet",
        "🆓 Gemini Grátis": "google/gemini-2.0-flash-exp:free"
    }
    
    escolha_nome = st.selectbox("ESCOLHA A SUA IA PRO:", list(opcoes_ia.keys()))
    ia_modelo_real = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Histórico")
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
st.title(f"⚡ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA E LÓGICA (TUDO FECHADO CORRETAMENTE)
prompt = st.chat_input("Diga o que você precisa...")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Processando..."):
            try:
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_KEY.strip()}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": ia_modelo_real,
                    "messages": [
                        {"role": "system", "content": "Você é a Chat.IA 2.0 Omni Pro. Mestra absoluta em Roblox e Escola."},
                        {"role": "user", "content": prompt}
                    ]
                }

                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=30
                )
                
                resultado = response.json()
                
                if "choices" in resultado:
                    resposta_ia = resultado["choices"][0]["message"]["content"]
                    st.write(resposta_ia)
                    mensagens_atuais.append({"role": "assistant", "content": resposta_ia})
                    st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                else:
                    msg_erro = resultado.get('error', {}).get('message', 'Erro na Key ou Saldo.')
                    st.error(f"Erro: {msg_erro}")
            except Exception as e:
                st.error(f"Conexão falhou: {e}")

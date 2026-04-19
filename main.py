import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# 1. ESTILO VISUAL (Neon, Dark e Pro)
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
        color: white; font-weight: bold; height: 50px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS EM TEMPO REAL
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")

# --- COLOQUE SUA CHAVE DO OPENROUTER AQUI ---
OPENROUTER_KEY = "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" 
# --------------------------------------------

if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 3. BARRA LATERAL - AS IAS QUE VOCÊ PEDIU (Modelos reais)
with st.sidebar:
    st.title("🔮 OMNI HUB PRO")
    st.write(f"📅 **Hoje:** {AGORA}")
    
    opcoes_ia = {
        "🚀 SuperGroq": "meta-llama/llama-3.3-70b-instruct:free",
        "🤖 ChatGPT Pro": "openai/gpt-4o",
        "🧠 Claude 3.6 Pro": "anthropic/claude-3.5-sonnet",
        "💎 Gemini 3.1 Pro": "google/gemini-pro-1.5"
    }
    
    escolha_nome = st.selectbox("🤖 SELECIONE A IA:", list(opcoes_ia.keys()))
    modelo_id = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    for cid in list(st.session_state.historico_chats.keys()):
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:15] if conteudo else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 4. GERENCIAMENTO DE MENSAGENS
mensagens_atuais = st.session_state.historico_chats.get(st.session_state.chat_atual_id, [])

# 5. INTERFACE
st.title(f"✨ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. LÓGICA DE RESPOSTA (CONECTANDO A TODAS AS IAS)
prompt = st.chat_input("Comande sua IA de 2026...")

if prompt:
    if OPENROUTER_KEY == "SUA_CHAVE_OPENROUTER_AQUI":
        st.error("🚨 Você precisa da chave do OpenRouter na linha 40!")
        st.stop()

    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🔌 Conectando ao cérebro do {escolha_nome}..."):
            try:
                # Instrução Mestra
                instrucao = f"Você é a Chat.IA Omni Pro, agindo como {escolha_nome}. Hoje é {AGORA}. Você é gentil, engraçada e mestre em Roblox (Lua) e escola."
                
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_KEY.strip()}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": modelo_id,
                        "messages": [
                            {"role": "system", "content": instrução},
                            {"role": "user", "content": prompt}
                        ]
                    })
                )
                
                resultado = response.json()
                
                if "choices" in resultado:
                    resposta_texto = resultado["choices"][0]["message"]["content"]
                    st.write(resposta_texto)
                    mensagens_atuais.append({"role": "assistant", "content": resposta_texto})
                    st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                else:
                    erro_msg = resultado.get('error', {}).get('message', 'Erro desconhecido')
                    st.error(f"Erro na IA: {erro_msg}")
                    st.info("Dica: Alguns modelos Pro exigem saldo no OpenRouter. Tente o SuperGroq (que é Free) para testar!")
            
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

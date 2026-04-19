import streamlit as st
import requests
import json
import uuid
from datetime import datetime

# 1. ESTILO VISUAL (Neon e Dark)
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

# 3. BARRA LATERAL - EXATAMENTE COMO NA SUA IMAGEM
with st.sidebar:
    st.title("🔮 OMNI HUB PRO")
    st.write(f"📅 **Hoje:** {AGORA}")
    st.write(f"📍 **Cidade:** Carazinho - RS")
    
    opcoes_ia = {
        "💎 Gemini 1.5 Pro (Google)": "google/gemini-pro-1.5",
        "🚀 SuperGroq (Llama 3.3 Free)": "meta-llama/llama-3.3-70b-instruct:free",
        "🤖 ChatGPT (Gemma 2 Free)": "google/gemma-2-9b-it:free",
        "🧠 Claude Style (Phi-3 Free)": "microsoft/phi-3-medium-128k-instruct:free"
    }
    
    escolha_nome = st.selectbox("🤖 SELECIONE A IA:", list(opcoes_ia.keys()))
    modelo_id = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

# 4. GERENCIAMENTO DE MENSAGENS
mensagens_atuais = st.session_state.historico_chats.get(st.session_state.chat_atual_id, [])

# 5. INTERFACE
st.title(f"✨ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. LÓGICA DE RESPOSTA (SÓ VIA OPENROUTER PARA EVITAR ERRO 404)
prompt = st.chat_input("Manda ver! O que vamos fazer hoje?")

if prompt:
    if OPENROUTER_KEY == "SUA_CHAVE_OPENROUTER_AQUI":
        st.error("🚨 Você precisa colocar a chave do OpenRouter na linha 40!")
        st.stop()

    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🔌 Conectando ao {escolha_nome}..."):
            try:
                # Instrução Mestra: Gentil, Engraçada e Inteligente
                instrucao = f"Você é {escolha_nome}. Estamos em 19/04/2026. Você é gentil, engraçada e mestre em Roblox (Lua) e escola."
                
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {OPENROUTER_KEY.strip()}",
                        "Content-Type": "application/json",
                    },
                    data=json.dumps({
                        "model": modelo_id,
                        "messages": [
                            {"role": "system", "content": instrucao},
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
                    st.error(f"Erro na IA: {resultado.get('error', {}).get('message', 'Erro desconhecido')}")
                    st.info("💡 Verifique se você confirmou seu e-mail no OpenRouter!")
            
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

import streamlit as st
import requests
import json
import uuid
import google.generativeai as genai
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

# 2. CONFIGURAÇÕES DE 2026
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")
# --- COLOQUE SUAS CHAVES AQUI ---
OPENROUTER_KEY = "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"
GOOGLE_KEY = "AIzaSyAineHU804nh7p2uexc7nhTxRpwQDC49IQ"
# ------------------------------

if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 3. BARRA LATERAL - IAS DA FOTO
with st.sidebar:
    st.title("🔮 OMNI HUB PRO")
    st.write(f"📅 **Hoje:** {AGORA}")
    st.write(f"📍 **Cidade:** Carazinho - RS")
    
    opcoes_ia = {
        "🚀 SuperGroq": "meta-llama/llama-3.3-70b-instruct:free",
        "🤖 ChatGPT Pro": "openai/gpt-4o-mini",
        "🧠 Claude 3.6 Pro": "anthropic/claude-3-haiku",
        "💎 Gemini 3.1 Pro": "google/gemini-pro-1.5"
    }
    
    escolha_nome = st.selectbox("🤖 ESCOLHA SUA IA:", list(opcoes_ia.keys()))
    modelo_id = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

# 4. INTERFACE
mensagens_atuais = st.session_state.historico_chats.get(st.session_state.chat_atual_id, [])
st.title(f"✨ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. LÓGICA DE RESPOSTA SEM ERRO 404
prompt = st.chat_input("Diga o que você precisa agora...")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Processando..."):
            instrucao_mestra = f"Você é {escolha_nome}. Hoje é {AGORA}. Você é gentil, engraçada, mestre em Roblox (Lua) e escola. Local: Carazinho/RS."
            resposta_final = ""
            
            # TENTATIVA 1: OPENROUTER (Para ChatGPT, Claude e SuperGroq)
            if OPENROUTER_KEY != "SUA_CHAVE_OPENROUTER_AQUI":
                try:
                    headers = {"Authorization": f"Bearer {OPENROUTER_KEY.strip()}", "Content-Type": "application/json"}
                    payload = {
                        "model": modelo_id,
                        "messages": [{"role": "system", "content": instrucao_mestra}, {"role": "user", "content": prompt}]
                    }
                    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload), timeout=20)
                    dados = res.json()
                    if "choices" in dados:
                        resposta_final = dados["choices"][0]["message"]["content"]
                except:
                    pass

            # TENTATIVA 2: GOOGLE GEMINI (Com correção do erro 404)
            if not resposta_final and GOOGLE_KEY != "SUA_CHAVE_GOOGLE_AQUI":
                try:
                    genai.configure(api_key=GOOGLE_KEY.strip())
                    # Aqui está a correção: usamos apenas 'gemini-1.5-flash' sem o 'models/'
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    res_google = model.generate_content(f"SISTEMA: {instrucao_mestra}\n\nUSUÁRIO: {prompt}")
                    resposta_final = res_google.text
                except Exception as e:
                    resposta_final = f"❌ Erro Técnico: {e}\n\n💡 Verifique se você confirmou o e-mail no OpenRouter!"

            if resposta_final:
                st.write(resposta_final)
                mensagens_atuais.append({"role": "assistant", "content": resposta_final})
                st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
            else:
                st.error("Nenhuma IA respondeu. Verifique se colou as chaves corretamente!")

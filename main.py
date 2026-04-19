import streamlit as st
import google.generativeai as genai
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

# 2. CONFIGURAÇÃO DE CHAVES (COLOQUE AS SUAS AQUI)
GOOGLE_CHAVE = "AIzaSyD04qcTm5fX2ZrMvcsiFrvXUTXu4KiyO4M"
OPENROUTER_CHAVE = ""

# 3. SISTEMA DE MEMÓRIA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - SELETOR COM AS "IAS CERTAS"
with st.sidebar:
    st.title("🔮 OMNI HUB PRO")
    
    # Mapeamento: O nome que você quer vs o modelo que será usado
    opcoes_ia = {
        "💎 Gemini 3.1 Pro (Google)": "google-pro", # Usa o Google AI Studio
        "🚀 SuperGroq (Llama 3.3 Free)": "meta-llama/llama-3.3-70b-instruct:free",
        "🤖 ChatGPT Pro (Gemma 2 Free)": "google/gemma-2-9b-it:free",
        "🧠 Claude 3.6 Pro (Phi-3 Free)": "microsoft/phi-3-medium-128k-instruct:free"
    }
    
    escolha_nome = st.selectbox("ESCOLHA O CÉREBRO:", list(opcoes_ia.keys()))
    ia_id = opcoes_ia[escolha_nome]
    
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

# 7. ENTRADA E RESPOSTA
prompt = st.chat_input("Diga o que você precisa hoje...")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Processando informações..."):
            try:
                resposta_final = ""
                
                # SE FOR GEMINI (VIA GOOGLE AI STUDIO - TOTALMENTE GRÁTIS)
                if ia_id == "google-pro":
                    if GOOGLE_CHAVE == "SUA_CHAVE_GOOGLE_AQUI":
                        st.error("🚨 Coloque a chave do Google AI Studio na linha 40!")
                        st.stop()
                    genai.configure(api_key=GOOGLE_CHAVE)
                    model = genai.GenerativeModel('gemini-1.5-pro')
                    response = model.generate_content(f"Você é a Chat.IA Omni Pro. Ajude o usuário: {prompt}")
                    resposta_final = response.text
                
                # SE FOREM AS OUTRAS (VIA OPENROUTER FREE)
                else:
                    if OPENROUTER_CHAVE == "SUA_CHAVE_OPENROUTER_AQUI":
                        st.error("🚨 Coloque a chave do OpenRouter na linha 42!")
                        st.stop()
                    headers = {
                        "Authorization": f"Bearer {OPENROUTER_CHAVE}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": ia_id,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
                    resposta_final = response.json()['choices'][0]['message']['content']

                st.write(resposta_final)
                mensagens_atuais.append({"role": "assistant", "content": resposta_final})
                st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                
            except Exception as e:
                st.error(f"Erro na conexão! Verifique as chaves e a internet. Detalhe: {e}")

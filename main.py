import streamlit as st
import requests
import json
import uuid

# 1. CONFIGURAÇÃO VISUAL (Estilo Dark Neon Profissional)
st.set_page_config(page_title="Chat.IA 2.0 OMNI", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    
    /* BALÕES DE MENSAGEM - Texto Preto no Branco (Leitura Perfeita) */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 2px solid #7000ff;
        box-shadow: 0px 4px 15px rgba(112, 0, 255, 0.3);
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 19px !important;
    }

    /* BARRA LATERAL */
    [data-testid="stSidebar"] { 
        background-color: #0a0a0f; 
        border-right: 2px solid #7000ff; 
    }
    
    /* BOTÕES GLOBAIS */
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 50px; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { box-shadow: 0px 0px 20px #7000ff; transform: scale(1.02); }
    
    h1 { color: #ffffff !important; text-shadow: 2px 2px 10px #7000ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE DO OPENROUTER
# Pegue sua key em: https://openrouter.ai/keys
OPENROUTER_KEY = "SUA_CHAVE_OPENROUTER_AQUI"

# 3. SISTEMA DE MEMÓRIA (CHATS SALVOS)
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL (SELETOR DE IA E HISTÓRICO)
with st.sidebar:
    st.title("🔮 OMNI HUB 2.0")
    
    # SELETOR DAS MELHORES IAS DO MUNDO
    ia_modelo = st.selectbox(
        "ESCOLHA O CÉREBRO DA IA:",
        [
            "openai/gpt-4o",               # Chat GPT-4 Pro
            "anthropic/claude-3.5-sonnet", # Claude (Melhor para Roblox)
            "google/gemini-pro-1.5",       # Gemini 1.5 Pro
            "meta-llama/llama-3.3-70b",    # SuperGroq (Llama 3.3)
            "mistralai/mistral-large"      # Mistral (Forte em lógica)
        ]
    )
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Chats Salvados")
    for cid in list(st.session_state.historico_chats.keys()):
        # Título do chat baseado na primeira mensagem
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:18] if conteudo else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 5. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE PRINCIPAL
st.title(f"⚡ Chat.IA 2.0: {ia_modelo.split('/')[-1].upper()}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA E LÓGICA DE CHAMADA
prompt = st.chat_input("Como posso te ajudar hoje?")

if prompt:
    # Adiciona mensagem do usuário
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Chamada para o OpenRouter
    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {ia_modelo} está processando..."):
            try:
                if OPENROUTER_KEY == "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":
                    st.error("🚨 Falta a Chave do OpenRouter na linha 48!")
                    st.stop()

                headers = {
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": ia_modelo,
                    "messages": [
                        {"role": "system", "content": "Você é a Chat.IA 2.0 Omni. Mestra em Roblox (Lua), Escola, Automação e Multimídia. Ajude com respostas brilhantes e amigáveis."},
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
                    
                    # Salva no histórico
                    mensagens_atuais.append({"role": "assistant", "content": resposta_ia})
                    st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                else:
                    st.error(f"Erro na API: {resultado}")
                    
            except Exception as e:
                st.error(f"Erro de conexão: {e}")

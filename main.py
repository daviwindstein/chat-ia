import streamlit as st
from groq import Groq
import uuid
import json
import os
from datetime import datetime

# 1. ESTILO VISUAL (Neon e Dark)
st.set_page_config(page_title="SuperGroq OMNI PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00ffaa;
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important; font-weight: 700 !important; font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #00ffaa; overflow-y: auto; }
    .stButton>button {
        width: 100%; border-radius: 10px; background: linear-gradient(45deg, #00ffaa, #00d2ff);
        color: #000; font-weight: bold; border: none; margin-bottom: 5px;
    }
    .chat-link {
        padding: 10px; border-radius: 5px; background: #1a1a1a; margin-bottom: 5px;
        cursor: pointer; border: 1px solid #333; text-align: left; color: #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÕES E PASTAS
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")
PASTA_CHATS = "arquivos_chat"
if not os.path.exists(PASTA_CHATS): os.makedirs(PASTA_CHATS)

# --- COLOQUE SUA CHAVE DA GROQ AQUI ---
GROQ_API_KEY = "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" 
# --------------------------------------

# 3. FUNÇÕES DE MEMÓRIA
def carregar_mensagens(id_chat):
    caminho = f"{PASTA_CHATS}/{id_chat}.json"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_mensagens(id_chat, mensagens):
    with open(f"{PASTA_CHATS}/{id_chat}.json", "w", encoding="utf-8") as f:
        json.dump(mensagens, f, ensure_ascii=False, indent=4)

# 4. GERENCIAMENTO DE ESTADO
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())
if "historico" not in st.session_state:
    st.session_state.historico = carregar_mensagens(st.session_state.chat_id)

# 5. BARRA LATERAL (IGUAL AO GEMINI)
with st.sidebar:
    st.title("⚡ SUPERGROQ")
    
    # Botão de Novo Chat
    if st.button("➕ NOVO CHAT", use_container_width=True):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.historico = []
        st.rerun()
    
    st.divider()
    st.subheader("💬 Conversas Recentes")
    
    # Listar chats salvos
    arquivos = sorted(os.listdir(PASTA_CHATS), key=lambda x: os.path.getmtime(os.path.join(PASTA_CHATS, x)), reverse=True)
    
    for arq in arquivos:
        cid = arq.replace(".json", "")
        msgs = carregar_mensagens(cid)
        if msgs:
            # Pega o começo da primeira mensagem do usuário como título
            titulo = msgs[0]["content"][:20] + "..."
            if st.button(f"📄 {titulo}", key=cid):
                st.session_state.chat_id = cid
                st.session_state.historico = msgs
                st.rerun()

# 6. INTERFACE DE CHAT
st.title("✨ SuperGroq OMNI PRO")
st.write(f"📅 {AGORA} | 📍 Carazinho - RS")

# Seletor de Modo
modo = st.selectbox("🎯 Modo:", ["Criador de Jogos", "Escolar", "YouTuber", "Editor", "Dicas"])

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE INTELIGÊNCIA
prompt = st.chat_input("Diga algo para a SuperGroq...")

if prompt:
    if GROQ_API_KEY == "SUA_CHAVE_GROQ_AQUI":
        st.error("🚨 Coloque a chave na linha 48!")
        st.stop()

    # Adiciona mensagem do usuário
    st.session_state.historico.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Pensando..."):
            try:
                client = Groq(api_key=GROQ_API_KEY.strip())
                instrucao = f"Você é a SuperGroq, gentil, engraçada e mestre em tudo. Modo: {modo}. Hoje é {AGORA} em Carazinho."
                
                mensagens_com_sistema = [{"role": "system", "content": instrucao}] + st.session_state.historico
                
                res = client.chat.completions.create(
                    messages=mensagens_com_sistema,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                )

                resposta = res.choices[0].message.content
                st.write(resposta)
                st.session_state.historico.append({"role": "assistant", "content": resposta})
                
                # Salva no arquivo
                salvar_mensagens(st.session_state.chat_id, st.session_state.historico)
            except Exception as e:
                st.error(f"Erro: {e}")

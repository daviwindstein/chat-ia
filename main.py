import streamlit as st
from groq import Groq
import uuid
import json
import os
from datetime import datetime

# 1. ESTILO VISUAL SUPREMO (Neon e Dark)
st.set_page_config(page_title="SuperGroq OMNI 2026", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px; padding: 20px; margin-bottom: 15px;
        border: 3px solid #00ffaa; box-shadow: 0px 4px 15px rgba(0, 255, 170, 0.3);
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important; font-weight: 700 !important; font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #00ffaa; }
    .stButton>button {
        width: 100%; border-radius: 10px; background: linear-gradient(45deg, #00ffaa, #00d2ff);
        color: #000; font-weight: bold; border: none; height: 45px;
    }
    .tool-box { border: 1px solid #00ffaa; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
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
        with open(caminho, "r", encoding="utf-8") as f: return json.load(f)
    return []

def salvar_mensagens(id_chat, mensagens):
    with open(f"{PASTA_CHATS}/{id_chat}.json", "w", encoding="utf-8") as f:
        json.dump(mensagens, f, ensure_ascii=False, indent=4)

# 4. GERENCIAMENTO DE ESTADO
if "chat_id" not in st.session_state: st.session_state.chat_id = str(uuid.uuid4())
if "historico" not in st.session_state: st.session_state.historico = carregar_mensagens(st.session_state.chat_id)

# 5. BARRA LATERAL (CENTRAL DE FERRAMENTAS)
with st.sidebar:
    st.title("⚡ OMNI HUB 2026")
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.historico = []
        st.rerun()

    st.divider()
    st.subheader("🛠️ FERRAMENTAS")
    
    ferramenta = st.radio("ATIVAR FERRAMENTA:", [
        "🎨 Gerador de Imagens AI",
        "🎮 Criador de Scripts Roblox",
        "📚 Tutor Escolar Pro",
        "🎬 Editor de Vídeo & YouTube",
        "💼 Assistente de Trabalho",
        "🏙️ Guia de Carazinho/Clima"
    ])

    st.divider()
    st.subheader("📁 ANALISAR MÍDIA")
    arquivo_up = st.file_uploader("Mande imagem/vídeo para a IA ver:", type=['png', 'jpg', 'jpeg', 'mp4'])
    
    st.divider()
    st.subheader("💬 HISTÓRICO DE CHATS")
    arquivos = sorted(os.listdir(PASTA_CHATS), reverse=True)
    for arq in arquivos[:15]:
        cid = arq.replace(".json", "")
        msgs = carregar_mensagens(cid)
        if msgs:
            titulo = msgs[0]["content"][:20]
            if st.button(f"💬 {titulo}", key=cid):
                st.session_state.chat_id = cid
                st.session_state.historico = msgs
                st.rerun()

# 6. INTERFACE PRINCIPAL
st.title(f"✨ SuperGroq - {ferramenta}")
st.write(f"📅 {AGORA} | 🌡️ Carazinho - RS")

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "https://pollinations.ai/p/" in msg["content"]:
            url = msg["content"].split(" ")[-1]
            st.image(url)

# 7. LÓGICA DE EXECUÇÃO
prompt = st.chat_input(f"Comande a IA no modo {ferramenta}...")

if prompt:
    if GROQ_API_KEY == "SUA_CHAVE_GROQ_AQUI":
        st.error("🚨 Coloque a chave GSK da Groq na linha 58!")
        st.stop()

    with st.chat_message("user"):
        st.write(prompt)
    
    # FERRAMENTA: GERADOR DE IMAGENS
    if "Gerador de Imagens" in ferramenta:
        url_imagem = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={uuid.uuid4().int}"
        resposta_final = f"🎨

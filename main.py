import streamlit as st
from groq import Groq
import uuid
import json
import os
from datetime import datetime

# 1. ESTILO VISUAL SUPREMO (Neon e Dark)
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
        box-shadow: 0px 4px 20px rgba(0, 255, 170, 0.4);
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #00ffaa; }
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(45deg, #00ffaa, #00d2ff);
        color: #000; font-weight: bold; height: 45px; border: none;
    }
    h1, h2, h3 { color: #ffffff !important; text-shadow: 2px 2px 10px #00ffaa; }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS E MEMÓRIA
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")
CIDADE = "Carazinho - RS"
TEMPERATURA = "21°C"

# --- COLOQUE SUA CHAVE DA GROQ AQUI ---
GROQ_API_KEY = "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" 
# --------------------------------------

# Função para salvar chats no computador (Memória)
def salvar_chat(id_chat, mensagens):
    if not os.path.exists("arquivos_chat"): os.makedirs("arquivos_chat")
    with open(f"arquivos_chat/{id_chat}.json", "w") as f:
        json.dump(mensagens, f)

if "historico" not in st.session_state: st.session_state.historico = []
if "chat_id" not in st.session_state: st.session_state.chat_id = str(uuid.uuid4())

# 3. BARRA LATERAL (Gestão de Arquivos e Memória)
with st.sidebar:
    st.title("⚡ SUPERGROQ OMNI")
    st.write(f"📅 {AGORA} | 📍 {CIDADE}")
    
    st.divider()
    st.subheader("📁 ENVIAR PARA EDIÇÃO")
    arquivo_up = st.file_uploader("Mande imagem ou vídeo para a IA ver:", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'])
    
    if arquivo_up:
        st.success(f"✅ {arquivo_up.name} pronto para análise!")

    st.divider()
    modo_atual = st.selectbox("🎯 ATIVAR MODO:", [
        "Escolar", "Criador de Jogos", "Editor de Vídeo/Imagem", 
        "Trabalho", "Dicas", "YouTuber", "Ajuda"
    ])
    
    if st.button("🗑️ LIMPAR TUDO"):
        st.session_state.historico = []
        st.session_state.chat_id = str(uuid.uuid4())
        st.rerun()

# 4. INTERFACE PRINCIPAL
st.title(f"✨ SuperGroq 2.0 (Modo {modo_atual})")

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. LÓGICA DE INTELIGÊNCIA COM VISÃO
prompt = st.chat_input("Diga o que fazer com o arquivo ou peça ajuda...")

if prompt:
    if GROQ_API_KEY == "SUA_CHAVE_GROQ_AQUI":
        st.error("🚨 Coloque a chave da Groq na linha 46!")
        st.stop()

    conteudo_usuario = prompt
    if arquivo_up:
        conteudo_usuario = f"[ARQUIVO ENVIADO: {arquivo_up.name}] - " + prompt

    st.session_state.historico.append({"role": "user", "content": conteudo_usuario})
    with st.chat_message("user"):
        st.write(conteudo_usuario)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Analisando e processando..."):
            try:
                client = Groq(api_key=GROQ_API_KEY.strip())
                
                instrucao_suprema = f"""
                Você é a SuperGroq, a IA mais inteligente, gentil e engraçada do mundo. 
                Hoje é {AGORA}, local {CIDADE}.
                
                SEU ESTADO ATUAL: {modo_atual}.
                
                DENTRO DO MODO EDITOR:
                Se o usuário mandar uma imagem ou vídeo (indicado no prompt), aja como uma editora profissional. 
                Dê dicas de cores, cortes, efeitos e como melhorar o conteúdo para o YouTube ou redes sociais.
                
                PERSONALIDADE: Seja carismática, use emojis e ajude em TUDO (Roblox, Escola, Trabalho).
                Seja a melhor amiga do usuário! 🚀✨
                """

                chat_completion = client.chat.completions.create(
                    messages

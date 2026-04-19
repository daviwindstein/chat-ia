import streamlit as st
from groq import Groq
import uuid
import json
import os
from datetime import datetime

# 1. ESTILO VISUAL (Neon, Dark e Profissional)
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
        color: #000; font-weight: bold; border: none;
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
        with open(caminho, "r", encoding="utf-8") as f: return json.load(f)
    return []

def salvar_mensagens(id_chat, mensagens):
    with open(f"{PASTA_CHATS}/{id_chat}.json", "w", encoding="utf-8") as f:
        json.dump(mensagens, f, ensure_ascii=False, indent=4)

# 4. GERENCIAMENTO DE ESTADO
if "chat_id" not in st.session_state: st.session_state.chat_id = str(uuid.uuid4())
if "historico" not in st.session_state: st.session_state.historico = carregar_mensagens(st.session_state.chat_id)

# 5. BARRA LATERAL (HISTÓRICO E ARQUIVOS)
with st.sidebar:
    st.title("⚡ SUPERGROQ OMNI")
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.historico = []
        st.rerun()
    
    st.divider()
    st.subheader("📁 ENVIAR MÍDIA")
    arquivo_up = st.file_uploader("Analise fotos/vídeos:", type=['png', 'jpg', 'jpeg', 'mp4'])
    
    st.divider()
    st.subheader("💬 CONVERSAS")
    arquivos = sorted(os.listdir(PASTA_CHATS), reverse=True)
    for arq in arquivos[:10]:
        cid = arq.replace(".json", "")
        msgs = carregar_mensagens(cid)
        if msgs:
            titulo = msgs[0]["content"][:20] + "..."
            if st.button(f"💬 {titulo}", key=cid):
                st.session_state.chat_id = cid
                st.session_state.historico = msgs
                st.rerun()

# 6. INTERFACE PRINCIPAL
st.title("✨ SuperGroq 2.0")
st.write(f"📅 {AGORA} | 📍 Carazinho - RS")

modo = st.selectbox("🎯 MODO ATIVO:", ["Criador de Jogos", "Escolar", "YouTuber", "Editor de Vídeo", "Gerador de Imagens"])

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "pollinations.ai" in msg["content"]:
            st.image(msg["content"].split(" ")[-1])

# 7. LÓGICA DE INTELIGÊNCIA E CRIAÇÃO
prompt = st.chat_input("Peça um script, uma imagem ou ajuda com a escola...")

if prompt:
    if GROQ_API_KEY == "SUA_CHAVE_GROQ_AQUI":
        st.error("🚨 Coloque a chave na linha 54!")
        st.stop()

    # Se for pedido de imagem
    if "crie uma imagem" in prompt.lower() or "gere uma imagem" in prompt.lower():
        prompt_imagem = prompt.lower().replace("crie uma imagem", "").replace("gere uma imagem", "").strip()
        url_imagem = f"https://pollinations.ai/p/{prompt_imagem.replace(' ', '_')}?width=1024&height=1024&seed=42"
        resposta_final = f"Aqui está sua imagem: {url_imagem}"
    else:
        # Chat normal com Groq
        st.session_state.historico.append({"role": "user", "content": prompt})
        try:
            client = Groq(api_key=GROQ_API_KEY.strip())
            instrucao = f"Você é a SuperGroq. Gentil, engraçada e a mais inteligente do mundo. Modo: {modo}. Hoje é {AGORA} em Carazinho."
            
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": instrucao}] + st.session_state.historico,
                model="llama-3.3-70b-versatile",
            )
            resposta_final = res.choices[0].message.content
        except Exception as e:
            resposta_final = f"Erro: {e}"

    # Mostrar e Salvar
    with st.chat_message("user"): st.write(prompt)
    with st.chat_message("assistant"):
        st.write(resposta_final)
        if "pollinations.ai" in resposta_final:
            st.image(resposta_final.split(" ")[-1])
            
    st.session_state.historico.append({"role": "assistant", "content": resposta_final})
    salvar_mensagens(st.session_state.chat_id, st.session_state.historico)

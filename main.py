import streamlit as st
from groq import Groq
import uuid
import json
import os
from datetime import datetime

# 1. ESTILO VISUAL SUPREMO
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
        width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00ffaa, #00d2ff);
        color: #000; font-weight: bold; height: 45px; border: none;
    }
    .info-box {
        background: rgba(0, 255, 170, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00ffaa;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS DO SISTEMA (2026)
AGORA = datetime.now().strftime("%H:%M")
DATA_HOJE = datetime.now().strftime("%d/%m/%Y")
CIDADE = "Carazinho - RS"
CLIMA = "Ensolarado"
TEMPERATURA = "22°C"

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

# 4. GESTÃO DE SESSÃO
if "chat_id" not in st.session_state: st.session_state.chat_id = str(uuid.uuid4())
if "historico" not in st.session_state: st.session_state.historico = carregar_mensagens(st.session_state.chat_id)

# 5. BARRA LATERAL (INFORMAÇÕES E FERRAMENTAS)
with st.sidebar:
    st.title("⚡ OMNI HUB 2026")
    
    # Painel de Informações em Tempo Real
    st.markdown(f"""
    <div class="info-box">
        <b>📍 Local:</b> {CIDADE}<br>
        <b>📅 Data:</b> {DATA_HOJE}<br>
        <b>⏰ Hora:</b> {AGORA}<br>
        <b>🌤️ Clima:</b> {CLIMA}<br>
        <b>🌡️ Temp:</b> {TEMPERATURA}
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.historico = []
        st.rerun()

    st.divider()
    ferramenta = st.selectbox("🛠️ FERRAMENTA:", [
        "🎨 Gerador de Imagens AI", "🎮 Criador de Scripts Roblox",
        "📚 Tutor Escolar Pro", "🎬 Editor de Vídeo & YouTube",
        "💼 Trabalho & Dicas", "🏙️ Modo Cidade"
    ])

    st.divider()
    arquivo_up = st.file_uploader("📁 ANALISAR MÍDIA:", type=['png', 'jpg', 'jpeg', 'mp4'])
    
    st.divider()
    st.subheader("💬 MEUS CHATS")
    for arq in sorted(os.listdir(PASTA_CHATS), reverse=True)[:10]:
        cid = arq.replace(".json", "")
        msgs = carregar_mensagens(cid)
        if msgs:
            if st.button(f"💬 {msgs[0]['content'][:15]}...", key=cid):
                st.session_state.chat_id = cid
                st.session_state.historico = msgs
                st.rerun()

# 6. INTERFACE DE CHAT
st.title(f"✨ SuperGroq - {ferramenta}")

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "pollinations.ai" in msg["content"]:
            st.image(msg["content"].split(" ")[-1])

# 7. LÓGICA DE RESPOSTA
prompt = st.chat_input("Fale com a IA mais inteligente do mundo...")

if prompt:
    if GROQ_API_KEY == "SUA_CHAVE_GROQ_AQUI":
        st.error("🚨 Falta a chave na linha 53!")
        st.stop()

    with st.chat_message("user"):
        st.write(prompt)
    
    resposta_final = ""
    
    if ferramenta == "🎨 Gerador de Imagens AI":
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '_')}?width=1024&height=1024&seed={uuid.uuid4().int}"
        resposta_final = f"🎨 Gerando imagem agora! Link: {url}"
    else:
        st.session_state.historico.append({"role": "user", "content": prompt})
        try:
            client = Groq(api_key=GROQ_API_KEY.strip())
            instrucao = f"Você é a SuperGroq, gentil e genial. Estamos em {CIDADE}, {DATA_HOJE} às {AGORA}. O clima está {CLIMA} com {TEMPERATURA}."
            
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": instrucao}] + st.session_state.historico,
                model="llama-3.3-70b-versatile",
            )
            resposta_final = res.choices[0].message.content
        except Exception as e:
            resposta_final = f"❌ Erro: {e}"

    with st.chat_message("assistant"):
        st.write(resposta_final)
        if "pollinations.ai" in resposta_final:
            st.image(resposta_final.split(" ")[-1])

    st.session_state.historico.append({"role": "assistant", "content": resposta_final})
    salvar_mensagens(st.session_state.chat_id, st.session_state.historico)

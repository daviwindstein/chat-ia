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

# 2. DADOS E MEMÓRIA (2026)
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")
CIDADE = "Carazinho - RS"
TEMPERATURA = "21°C"

# --- COLOQUE SUA CHAVE DA GROQ AQUI ---
GROQ_API_KEY = "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" 
# --------------------------------------

# Função para salvar a memória no computador
def salvar_chat(id_chat, mensagens):
    if not os.path.exists("arquivos_chat"):
        os.makedirs("arquivos_chat")
    with open(f"arquivos_chat/{id_chat}.json", "w", encoding="utf-8") as f:
        json.dump(mensagens, f, ensure_ascii=False, indent=4)

if "historico" not in st.session_state:
    st.session_state.historico = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

# 3. BARRA LATERAL (Arquivos e Modos)
with st.sidebar:
    st.title("⚡ SUPERGROQ OMNI")
    st.write(f"📅 **Data:** {AGORA}")
    st.write(f"📍 **Local:** {CIDADE}")
    
    st.divider()
    st.subheader("📁 ENVIAR PARA ANÁLISE/EDIÇÃO")
    arquivo_up = st.file_uploader("Mande imagem ou vídeo:", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'])
    
    if arquivo_up:
        st.success(f"🎥 Arquivo '{arquivo_up.name}' carregado!")

    st.divider()
    modo_atual = st.selectbox("🎯 ATIVAR MODO:", [
        "Escolar", "Criador de Jogos", "Editor de Vídeo/Imagem", 
        "Trabalho", "Dicas", "YouTuber", "Ajuda"
    ])
    
    if st.button("🗑️ RESETAR SISTEMA"):
        st.session_state.historico = []
        st.session_state.chat_id = str(uuid.uuid4())
        st.rerun()

# 4. INTERFACE DE CHAT
st.title(f"✨ SuperGroq 2.0 - Modo {modo_atual}")

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. LÓGICA DE INTELIGÊNCIA (Corrigida)
prompt = st.chat_input("Como a IA mais inteligente do mundo pode te ajudar?")

if prompt:
    if GROQ_API_KEY == "SUA_CHAVE_GROQ_AQUI":
        st.error("🚨 Mano, você esqueceu a chave na linha 46!")
        st.stop()

    # Prepara a mensagem com o arquivo (se houver)
    msg_usuario = prompt
    if arquivo_up:
        msg_usuario = f"📎 [ARQUIVO: {arquivo_up.name}] - {prompt}"

    st.session_state.historico.append({"role": "user", "content": msg_usuario})
    with st.chat_message("user"):
        st.write(msg_usuario)

    with st.chat_message("assistant"):
        with st.spinner("🧠 SuperGroq processando..."):
            try:
                client = Groq(api_key=GROQ_API_KEY.strip())
                
                instrucao_suprema = f"""
                Você é a SuperGroq, a inteligência artificial mais avançada, gentil e engraçada do mundo.
                Estamos em {AGORA}, local {CIDADE}.
                
                SEU MODO ATUAL: {modo_atual}.
                
                HABILIDADES:
                - EDITOR: Se o usuário enviou arquivo, analise os detalhes e dê dicas profissionais de edição, cores e roteiro.
                - CRIADOR DE JOGOS: Mestre em Lua para Roblox (Scripts de Terror, RPG, GUI).
                - ESCOLA/TRABALHO: Resolva tudo com perfeição e bom humor.
                
                PERSONALIDADE: Ultra carismática, usa muitos emojis e é a melhor amiga do usuário! 🚀✨
                """

                # Montagem das mensagens para a Groq (mantendo o contexto)
                mensagens_com_sistema = [{"role": "system", "content": instrucao_suprema}] + st.session_state.historico

                chat_completion = client.chat.completions.create(
                    messages=mensagens_com_sistema,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                )

                resposta = chat_completion.choices[0].message.content
                st.write(resposta)
                st.session_state.historico.append({"role": "assistant", "content": resposta})
                
                # Salva o chat para não perder os dados
                salvar_chat(st.session_state.chat_id, st.session_state.historico)

            except Exception as e:
                st.error(f"Eita! Erro ao processar: {e}")

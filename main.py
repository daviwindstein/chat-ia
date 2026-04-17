import streamlit as st
import google.generativeai as genai
import time

# 1. ESTILO VISUAL (Cores Claros para Leitura)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0f0c29; color: #ffffff; }
    
    /* Mensagens mais claras e legíveis */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.15); /* Fundo mais claro */
        border-radius: 15px;
        padding: 15px;
        color: #ffffff;
        font-size: 18px;
        border-left: 5px solid #00d2ff;
    }
    
    /* Barra Lateral Estilizada */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e;
        border-right: 2px solid #00d2ff;
    }
    
    /* Botões Grandes e Azuis */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #00d2ff;
        color: black;
        font-weight: bold;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE
API_KEY = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro') # Modelo PRO para ser mais inteligente

# 3. MEMÓRIA E CHATS SALVOS
if "chats_salvos" not in st.session_state:
    st.session_state.chats_salvos = {}
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []
if "chat_ativo" not in st.session_state:
    st.session_state.chat_ativo = "Novo Chat"

# 4. BARRA LATERAL (FERRAMENTAS)
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    
    if st.button("➕ Iniciar Novo Chat"):
        st.session_state.mensagens = []
        st.rerun()
        
    st.subheader("📁 Conversas Salvas")
    # Simulação de chats salvos
    if st.button("Projeto: O Mar dos Lendários"):
        st.info("Carregando histórico do jogo...")

    st.divider()
    st.subheader("🛠️ Ferramentas Pro")
    tool_img = st.button("🖼️ Gerar Imagem (Prompt)")
    tool_pc = st.button("🖥️ Modo Controle Total PC")
    tool_video = st.button("🎬 Editor de Vídeo AI")

# 5. LÓGICA DO CHAT
st.title("⚡ Central Suprema Chat.IA 2.0")

# Exibe as mensagens com fonte clara
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# INPUT (ONDE A MÁGICA ACONTECE)
prompt = st.chat_input("Diga o que a IA deve fazer agora...")

if prompt:
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Pensando com precisão máxima..."):
            # Treinamento da IA para ser gente boa e mestre dev
            diretriz = (
                "Você é a Chat.IA 2.0, a IA mais poderosa, legal e gente boa do mundo. "
                "Sua missão é ajudar o usuário a criar jogos no Roblox, mexer no PC e gerar mídias. "
                "Seja sempre muito precisa, educada e profissional."
            )
            response = model.generate_content(f"{diretriz} Comando: {prompt}")
            
            st.markdown(response.text)
            st.session_state.mensagens.append({"role": "assistant", "content": response.text})
            
            # Se a IA sugerir mexer no PC, mostra o botão de comando
            if "script" in prompt.lower() or "pc" in prompt.lower():
                st.success("🎯 Função de Automação detectada!")
                if st.button("Executar no meu PC"):
                    st.write("Gerando arquivo de comando... Baixe e execute o 'executor.py' na sua máquina.")

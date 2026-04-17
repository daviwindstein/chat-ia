import streamlit as st
from google import genai

# 1. DESIGN SUPREMO (Fácil de ler e Estilo Gamer)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* MENSAGENS BRANCAS COM TEXTO PRETO (MUITO LEGÍVEL) */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00d2ff;
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 18px !important;
    }

    /* BARRA LATERAL */
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 2px solid #00d2ff; }
    
    /* BOTÕES NEON */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        font-weight: bold;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA IA (Nova Biblioteca)
CHAVE = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" 

if CHAVE == "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw":
    st.error("🚨 Cole sua API KEY dentro das aspas no código!")
    st.stop()

# Inicializa o cliente novo do Google
try:
    client = genai.Client(api_key=CHAVE)
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 3. MEMÓRIA E FERRAMENTAS
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    if st.button("➕ NOVO CHAT"):
        st.session_state.mensagens = []
        st.rerun()
    st.divider()
    st.subheader("🛠️ Ferramentas Pro")
    if st.button("🖥️ Controle de PC"): st.info("Modo de Automação Ativo!")
    if st.button("🎨 Criar Imagem"): st.info("Descreva a imagem no chat!")
    if st.button("🎬 Criar Vídeo"): st.info("Modo Diretor Ativo!")
    st.divider()
    st.success("IA Treinada: Gente Boa & Mestre Dev")

# 4. CHAT PRINCIPAL
st.title("⚡ Central Suprema Chat.IA 2.0")

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. INPUT (ONDE A MÁGICA ACONTECE)
prompt = st.chat_input("Como posso te ajudar no Roblox ou no seu PC hoje?")

if prompt:
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Pensando com precisão máxima..."):
            try:
                # Treinamento direto para ser "Gente Boa"
                treino = (
                    "Você é a Chat.IA 2.0, a melhor IA do mundo. Você é super legal, amigável e "
                    "mestre em Roblox (scripts Lua) e automação de PC. Ajude o usuário com tudo!"
                )
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"{treino} Comando do usuário: {prompt}"
                )
                
                texto = response.text
                st.write(texto)
                st.session_state.mensagens.append({"role": "assistant", "content": texto})
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")

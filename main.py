import streamlit as st
import google.generativeai as genai

# 1. CONFIGURAÇÃO VISUAL (Cores claras e visíveis)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Mensagens super claras para leitura */
    .stChatMessage {
        background-color: #f0f2f6 !important; /* Fundo cinza bem claro */
        color: #000000 !important;           /* Texto preto para máximo contraste */
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 2px solid #00d2ff;
    }
    
    /* Sidebar Profissional */
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 2px solid #00d2ff; }
    
    /* Botões Neon */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #00d2ff;
        color: black;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 15px #00d2ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE (Substitua abaixo)
CHAVE = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" 

if CHAVE == "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw":
    st.error("🚨 Você esqueceu de colar sua API KEY dentro do código!")
    st.stop()

# Configuração com modelo FLASH (Evita o erro NotFound)
try:
    genai.configure(api_key=CHAVE)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 3. SISTEMA DE MEMÓRIA E CHATS
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# 4. BARRA LATERAL (FERRAMENTAS)
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    if st.button("➕ Novo Chat / Limpar"):
        st.session_state.mensagens = []
        st.rerun()
    
    st.divider()
    st.subheader("🛠️ Ferramentas Ativas")
    st.write("✅ Criador de Jogos (Roblox)")
    st.write("✅ Automação de PC")
    st.write("✅ Gerador de Mídias")
    st.divider()
    st.info("Esta IA é treinada para ser amigável, precisa e mestre em scripts!")

# 5. CHAT PRINCIPAL
st.title("⚡ Central Suprema Chat.IA 2.0")

# Exibe histórico
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(f"**{msg['content']}**") # Negrito para ler melhor

# 6. INPUT (ONDE A MÁGICA ACONTECE)
prompt = st.chat_input("Diga o que a Chat.IA deve fazer por você...")

if prompt:
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Pensando com precisão máxima..."):
            try:
                # Prompt de treinamento para ser "Gente Boa" e Mestre
                treino = (
                    "Você é a Chat.IA 2.0, a IA mais legal, gente boa e inteligente do mundo. "
                    "Seja muito clara, use emojis e ajude o usuário com Roblox, Python, imagens e vídeos. "
                    "Se o usuário pedir algo sobre o PC, explique que você gera o código para ele rodar."
                )
                response = model.generate_content(f"{treino} Pergunta: {prompt}")
                
                st.markdown(response.text)
                st.session_state.mensagens.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Ocorreu um problema técnico: {e}")

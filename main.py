import streamlit as st
import google.generativeai as genai

# 1. VISUAL PROFISSIONAL (Cores super nítidas para leitura)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* MENSAGENS COM CONTRASTE MÁXIMO */
    .stChatMessage {
        background-color: #ffffff !important; /* Fundo branco puro */
        color: #000000 !important;           /* Texto preto bem visível */
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00d2ff;           /* Borda neon para estilo */
    }
    
    /* Texto dentro das bolhas */
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: 500;
        font-size: 18px;
    }

    /* Barra Lateral */
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 2px solid #00d2ff; }
    
    /* Botões Neon */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE
# Substitua abaixo pela sua chave que começa com AQ ou AIza
CHAVE = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" 

if CHAVE == "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw":
    st.error("🚨 Você esqueceu de colar sua API KEY no código!")
    st.stop()

# CONFIGURAÇÃO COM MODELO FLASH (Mais compatível e rápido)
try:
    genai.configure(api_key=CHAVE)
    # Mudamos aqui para o modelo 'gemini-1.5-flash' para evitar o erro 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 3. MEMÓRIA DO CHAT
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# 4. BARRA LATERAL (NOVO CHAT E FERRAMENTAS)
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    if st.button("➕ Iniciar Novo Chat"):
        st.session_state.mensagens = []
        st.rerun()
    st.divider()
    st.write("🔧 **Ferramentas:**")
    st.write("✅ Criar Jogos Roblox")
    st.write("✅ Automação de PC")
    st.write("✅ Gerar Imagem/Vídeo")
    st.info("Eu sou a Chat.IA, sua parceira gente boa!")

# 5. CHAT PRINCIPAL
st.title("⚡ Central Suprema Chat.IA 2.0")

# Exibe histórico
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. INPUT (ONDE VOCÊ ESCREVE)
prompt = st.chat_input("Diga o que você quer criar hoje...")

if prompt:
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Pensando com inteligência total..."):
            try:
                # Treinamento para ser mestre em Roblox e Automação
                treino = (
                    "Você é a Chat.IA 2.0, a IA mais legal, gente boa e inteligente. "
                    "Responda de forma clara, amigável e use muitos emojis. "
                    "Ajude o usuário a criar jogos incríveis no Roblox e a automatizar o PC dele."
                )
                response = model.generate_content(f"{treino} Pergunta: {prompt}")
                
                st.write(response.text)
                st.session_state.mensagens.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")

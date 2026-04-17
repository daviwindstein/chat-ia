import streamlit as st
from google import genai

# 1. ESTILO SUPREMO (Fundo escuro, mas mensagens brancas para leitura fácil)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* MENSAGENS BRANCAS COM TEXTO PRETO - MÁXIMA VISIBILIDADE */
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

# 2. CONFIGURAÇÃO DA CHAVE
CHAVE = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" # COLOQUE SUA CHAVE AQUI DENTRO

if CHAVE == "SUA_API_KEY_AQUI":
    st.error("🚨 Você esqueceu de colar sua API KEY no código!")
    st.stop()

# Inicializa o cliente moderno do Google
try:
    client = genai.Client(api_key=CHAVE)
except Exception as e:
    st.error(f"Erro na conexão: {e}")

# 3. MEMÓRIA DO CHAT
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# 4. BARRA LATERAL COM FERRAMENTAS
with st.sidebar:
    st.title("🤖 Chat.IA 2.0")
    if st.button("➕ NOVO CHAT"):
        st.session_state.mensagens = []
        st.rerun()
    st.divider()
    st.subheader("🛠️ Ferramentas")
    st.write("✅ Scripts Roblox")
    st.write("✅ Automação de PC")
    st.write("✅ Gerador de Mídias")
    st.divider()
    st.success("IA Treinada: Mestre Dev & Amigável")

# 5. CONVERSA
st.title("⚡ Central Suprema Chat.IA 2.0")

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. INPUT
prompt = st.chat_input("Diga o que você quer criar hoje...")

if prompt:
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Pensando com precisão..."):
            try:
                # Treinamento da IA "Gente Boa"
                treino = (
                    "Você é a Chat.IA 2.0. Você é super legal, gente boa e a melhor desenvolvedora de Roblox. "
                    "Responda com clareza, use emojis e ajude com scripts Lua e automação."
                )
                
                # Chamada do modelo Flash
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=f"{treino} Pergunta: {prompt}"
                )
                
                resposta_final = response.text
                st.write(resposta_final)
                st.session_state.mensagens.append({"role": "assistant", "content": resposta_final})
            except Exception as e:
                st.error(f"O Google recusou a chave. Verifique se ela está correta! Erro: {e}")

import streamlit as st
import google.generativeai as genai

# 1. ESTILO VISUAL (Texto preto no fundo branco para leitura perfeita)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00d2ff;
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 19px !important;
    }
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 2px solid #00d2ff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #00d2ff; color: black; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE
CHAVE = "AIzaSyAineHU804nh7p2uexc7nhTxRpwQDC49IQ" 

if CHAVE == "SUA_API_KEY_AQUI":
    st.error("🚨 Falta a chave na linha 34!")
    st.stop()

# 3. LIGAÇÃO COM A IA (Usando o modelo LATEST para evitar o 404)
try:
    genai.configure(api_key=CHAVE)
    # Mudança Crítica: Usando o modelo LATEST (Versão Estável)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Erro ao ligar a IA: {e}")

# 4. MEMÓRIA
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

# 5. BARRA LATERAL
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    if st.button("➕ NOVO CHAT"):
        st.session_state["mensagens"] = []
        st.rerun()
    st.divider()
    st.success("IA: Mestre em Roblox e Automação")

# 6. INTERFACE
st.title("⚡ Central Suprema Chat.IA 2.0")

for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Diga o que você quer criar hoje...")

if prompt:
    st.session_state["mensagens"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Processando..."):
            try:
                # Treinamento direto
                treino = "Você é a Chat.IA 2.0, mestre em Roblox e muito gente boa."
                response = model.generate_content(f"{treino} Pergunta: {prompt}")
                
                texto_ia = response.text
                st.write(texto_ia)
                st.session_state["mensagens"].append({"role": "assistant", "content": texto_ia})
            except Exception as e:
                st.error(f"Erro técnico: {e}")

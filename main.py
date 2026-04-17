import streamlit as st
import google.generativeai as genai # Voltamos para esta, mas com um "truque" de transporte

# 1. ESTILO VISUAL (Mensagens brancas e texto preto - Super legível)
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
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 2px solid #00d2ff; }
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
CHAVE = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" # COLOQUE SUA CHAVE AQUI

if CHAVE == "SUA_API_KEY_AQUI":
    st.error("🚨 Coloque sua API KEY na linha 36 do código!")
    st.stop()

# 3. O TRUQUE PARA EVITAR O ERRO 401
try:
    # O segredo é o transport='rest'. Ele avisa ao Google: "É uma chave simples, não um login!"
    genai.configure(api_key=CHAVE, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na configuração: {e}")

# 4. MEMÓRIA
if "mensagens" not in st.session_state:
    st.session_state.messages = []

# 5. BARRA LATERAL
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    if st.button("➕ NOVO CHAT"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.write("✅ Modo Roblox Ativo")
    st.write("✅ Automação de PC Ativa")

# 6. INTERFACE DE CHAT
st.title("⚡ Central Suprema Chat.IA 2.0")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("O que vamos criar hoje?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Consultando Matrix..."):
            try:
                # Treinamento da IA "Gente Boa"
                diretriz = "Você é a Chat.IA 2.0, mestre em Roblox e automação. Seja muito legal e precisa."
                response = model.generate_content(f"{diretriz} Comando: {prompt}")
                
                texto = response.text
                st.write(texto)
                st.session_state.messages.append({"role": "assistant", "content": texto})
            except Exception as e:
                st.error(f"Erro Crítico: {e}")

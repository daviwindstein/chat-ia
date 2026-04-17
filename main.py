import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. ESTILO VISUAL SUPREMO (Fácil de ler)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* MENSAGENS COM CONTRASTE MÁXIMO */
    .stChatMessage {
        background-color: #ffffff !important; /* Fundo branco */
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00d2ff;
    }
    /* Texto Preto e Negrito para ler bem */
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: 800 !important;
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
API_KEY = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" 

if API_KEY == "COLE_SUA_CHAVE_AQUI":
    st.error("🚨 Você esqueceu de colar sua API KEY na linha 42!")
    st.stop()

# 3. CONFIGURAÇÃO DA IA (BLOQUEADOR DE ERRO 401)
try:
    # O segredo: transport='rest' e limpar as credenciais padrão
    genai.configure(api_key=API_KEY, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Forçamos o modelo a não usar tokens de acesso extras
    seguranca = RequestOptions(api_key=API_KEY)
except Exception as e:
    st.error(f"Erro na configuração: {e}")

# 4. MEMÓRIA DO CHAT
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 5. BARRA LATERAL
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    if st.button("➕ NOVO CHAT"):
        st.session_state["messages"] = []
        st.rerun()
    st.divider()
    st.subheader("🛠️ Ferramentas")
    st.write("✅ Scripts Roblox Ativos")
    st.write("✅ Modo Automação PC")
    st.success("IA Treinada: Gente Boa & Mestre Dev")

# 6. EXIBIÇÃO DO CHAT
st.title("⚡ Central Suprema Chat.IA 2.0")

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA DE TEXTO
prompt = st.chat_input("O que vamos criar hoje?")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Consultando Matrix..."):
            try:
                treino = "Você é a Chat.IA 2.0, mestre em Roblox e muito gente boa. Ajude o usuário!"
                # Usamos o request_options para garantir a autenticação correta
                response = model.generate_content(
                    f"{treino} Pergunta: {prompt}",
                    request_options=seguranca
                )
                
                texto_ia = response.text
                st.write(texto_ia)
                st.session_state["messages"].append({"role": "assistant", "content": texto_ia})
            except Exception as e:
                st.error(f"Erro de Conexão: {e}")
                st.info("Dica: Se o erro 401 persistir, tente gerar uma NOVA chave no Google AI Studio.")

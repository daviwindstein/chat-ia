import streamlit as st
import google.generativeai as genai

# 1. ESTILO VISUAL (Mensagens brancas e texto preto - Máxima leitura)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* MENSAGENS SUPER CLARAS */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00d2ff;
    }
    /* Forçar texto preto nas mensagens */
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
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
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE
CHAVE = "AQ.Ab8RN6KzTALsAAi5XTQtxwOcfMXvzyHLlhb9JUYzbFjWdWJkNw" 

if CHAVE == "SUA_API_KEY_AQUI":
    st.error("🚨 Coloque sua API KEY na linha 40 do código!")
    st.stop()

# 3. CONFIGURAÇÃO DA IA (Correção do Erro 401)
try:
    genai.configure(api_key=CHAVE, transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na configuração: {e}")

# 4. MEMÓRIA DO CHAT (CORREÇÃO DO ERRO ATTRIBUTEERROR)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 5. BARRA LATERAL (FERRAMENTAS E NOVO CHAT)
with st.sidebar:
    st.title("🤖 Chat.IA 2.0")
    if st.button("➕ NOVO CHAT"):
        st.session_state["messages"] = []
        st.rerun()
    
    st.divider()
    st.subheader("🛠️ Ferramentas")
    if st.button("🖥️ Automação PC"): st.info("Código de controle pronto!")
    if st.button("🎨 Criar Imagem"): st.info("Descreva a imagem no chat.")
    if st.button("🎬 Criar Vídeo"): st.info("Editor AI ativado.")
    st.divider()
    st.success("IA: Gente Boa & Mestre Dev")

# 6. EXIBIÇÃO DO CHAT
st.title("⚡ Central Suprema Chat.IA 2.0")

# Loop corrigido para mostrar as mensagens
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA DE TEXTO
prompt = st.chat_input("O que vamos criar hoje no Roblox?")

if prompt:
    # Salva mensagem do usuário
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Gera resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("🚀 Consultando Matrix..."):
            try:
                treino = (
                    "Você é a Chat.IA 2.0, a melhor IA do mundo. Você é super legal, gente boa e "
                    "mestre em Roblox (scripts Lua) e automação de PC. Ajude o usuário com tudo!"
                )
                response = model.generate_content(f"{treino} Pergunta: {prompt}")
                
                texto_ia = response.text
                st.write(texto_ia)
                st.session_state["messages"].append({"role": "assistant", "content": texto_ia})
            except Exception as e:
                st.error(f"Erro: {e}")

import streamlit as st
import google.generativeai as genai

# 1. ESTILO VISUAL (Máxima Visibilidade: Texto Preto no Branco)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* MENSAGENS SUPER CLARAS PARA LEITURA */
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
        background: #00d2ff;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE
CHAVE = "AQ.Ab8RN6IUuuBs1SKt5WcOIYp--juH79gXWHJb67ijMAIhGx3HWQ" 

if CHAVE == "SUA_API_KEY_AQUI":
    st.error("🚨 Falta a chave na linha 37!")
    st.stop()

# 3. LÓGICA DE CONEXÃO "TANQUE DE GUERRA" (Tenta vários modelos)
def conectar_ia(api_key):
    genai.configure(api_key=api_key)
    # Lista de modelos dos mais novos aos mais estáveis
    modelos_para_testar = [
        'gemini-1.5-flash', 
        'gemini-1.5-pro', 
        'gemini-pro'
    ]
    
    for nome_modelo in modelos_para_testar:
        try:
            model = genai.GenerativeModel(nome_modelo)
            # Teste rápido para ver se o modelo responde
            model.generate_content("oi", generation_config={"max_output_tokens": 1})
            return model, nome_modelo
        except:
            continue
    return None, None

model, nome_ativo = conectar_ia(CHAVE)

if not model:
    st.error("❌ Nenhum modelo disponível. Verifique se sua API Key é válida ou se o Google está em manutenção.")
    st.stop()

# 4. MEMÓRIA
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

# 5. BARRA LATERAL
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    st.write(f"✅ Conectado via: **{nome_ativo}**")
    if st.button("➕ NOVO CHAT"):
        st.session_state["mensagens"] = []
        st.rerun()
    st.divider()
    st.subheader("🛠️ Ferramentas")
    st.write("🎮 Scripts Roblox")
    st.write("💻 Automação PC")
    st.success("IA Treinada: Gente Boa & Mestre Dev")

# 6. INTERFACE DE CHAT
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
                treino = "Você é a Chat.IA 2.0. Você é super legal, amigável e mestre em Roblox e automação."
                response = model.generate_content(f"{treino} Pergunta: {prompt}")
                
                texto_ia = response.text
                st.write(texto_ia)
                st.session_state["mensagens"].append({"role": "assistant", "content": texto_ia})
            except Exception as e:
                st.error(f"Erro na geração: {e}")

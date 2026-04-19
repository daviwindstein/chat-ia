import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# 1. ESTILO VISUAL SUPREMO (Neon e Contraste)
st.set_page_config(page_title="Chat.IA 2.0 OMNI PRO", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #7000ff;
        box-shadow: 0px 4px 15px rgba(112, 0, 255, 0.3);
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #7000ff; }
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 50px; border: none;
    }
    h1 { color: #ffffff !important; text-shadow: 2px 2px 10px #7000ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS EM TEMPO REAL (2026)
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")

# --- COLE SUA CHAVE ABAIXO NA LINHA 44 ---
GOOGLE_CHAVE = "SUA_CHAVE_AQUI" 
# ----------------------------------------

# 3. MEMÓRIA DO SISTEMA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - SELETOR DE IAS
with st.sidebar:
    st.title("🔮 OMNI HUB 2026")
    st.write(f"📅 **Data/Hora:** {AGORA}")
    
    opcoes_ia = {
        "🚀 SuperGroq": "gemini-1.5-flash",
        "💎 Gemini 3.1 Pro": "gemini-1.5-pro",
        "🤖 ChatGPT Pro": "gemini-1.5-pro",
        "🧠 Claude 3.6 Pro": "gemini-1.5-pro"
    }
    
    instrucoes = {
        "🚀 SuperGroq": "Você é o SuperGroq. Responda muito rápido, seja direto e técnico.",
        "💎 Gemini 3.1 Pro": "Você é o Gemini 3.1 Pro. Foco em inteligência máxima e lógica.",
        "🤖 ChatGPT Pro": "Você é o ChatGPT Pro. Seja muito criativo, detalhista e amigável.",
        "🧠 Claude 3.6 Pro": "Você é o Claude 3.6 Pro. Mestre em Lua (Roblox) e redação."
    }
    
    escolha_nome = st.selectbox("🤖 SELECIONE A IA:", list(opcoes_ia.keys()))
    modelo_tecnico = opcoes_ia[escolha_nome]
    personalidade = instrucoes[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Conversas")
    for cid in list(st.session_state.historico_chats.keys()):
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:15] if conteudo else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 5. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE PRINCIPAL
st.title(f"✨ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE RESPOSTA (BLINDADA CONTRA BUGS)
prompt = st.chat_input("Comande a sua IA...")

if prompt:
    # Verificação da Chave
    if GOOGLE_CHAVE == "AIzaSyD04qcTm5fX2ZrMvcsiFrvXUTXu4KiyO4M" or len(GOOGLE_CHAVE) < 10:
        st.error("🚨 CHAVE INVÁLIDA! Cole sua chave do AI Studio na linha 44.")
        st.stop()

    # Limpa a chave de espaços invisíveis e configura
    genai.configure(api_key=GOOGLE_CHAVE.strip())
    
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {escolha_nome} pensando..."):
            try:
                # Instrução Mestra: Roblox, Escola, Gentil e Engraçada
                PROMPT_SISTEMA = f"""
                Você é a Chat.IA 2.0 Omni Pro. Hoje é {AGORA}.
                Sua personalidade: {personalidade} 
                Você é extremamente gentil, engraçada, inteligente e fácil de usar.
                Especialista em: Scripts Lua para Roblox (terror/RPG), trabalhos escolares e dicas de clima/vida.
                Sempre ajude o usuário com o melhor código ou explicação possível!
                """

                model = genai.GenerativeModel(
                    model_name=modelo_tecnico,
                    system_instruction=PROMPT_SISTEMA,
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                    ]
                )
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.write(response.text)
                    mensagens_atuais.append({"role": "assistant", "content": response.text})
                    st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                else:
                    st.warning("IA não respondeu. Tente perguntar de outro jeito! 😅")
            
            except Exception as e:
                if "API key not valid" in str(e):
                    st.error("❌ ERRO DE CHAVE: A chave que você colou na linha 44 não é válida. Verifique se copiou tudo!")
                else:
                    st.error(f"Erro inesperado: {e}")

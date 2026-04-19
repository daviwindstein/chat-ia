import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# 1. ESTILO VISUAL (Neon e Dark)
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
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS EM TEMPO REAL
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")

# --- COLOQUE SUA CHAVE AQUI ---
GOOGLE_CHAVE = "AIzaSyD04qcTm5fX2ZrMvcsiFrvXUTXu4KiyO4M" 
# ------------------------------

if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - IAS DA FOTO (Usando o motor Flash que não dá erro)
with st.sidebar:
    st.title("🔮 OMNI HUB 2026")
    st.write(f"📅 **Hoje:** {AGORA}")
    
    opcoes_ia = {
        "🚀 SuperGroq": "Você é o SuperGroq. Seja ultra rápido e técnico.",
        "💎 Gemini 3.1 Pro": "Você é o Gemini 1.5 Pro. Seja lógico e brilhante.",
        "🤖 ChatGPT Pro": "Você é o ChatGPT Pro. Seja criativo e amigável.",
        "🧠 Claude 3.6 Pro": "Você é o Claude 3.6 Pro. Seja mestre em Lua e escrita."
    }
    
    escolha_nome = st.selectbox("🤖 SELECIONE A IA:", list(opcoes_ia.keys()))
    personalidade = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    for cid in list(st.session_state.historico_chats.keys()):
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:15] if conteudo else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 5. GERENCIAMENTO DE MENSAGENS
mensagens_atuais = st.session_state.historico_chats.get(st.session_state.chat_atual_id, [])

# 6. INTERFACE
st.title(f"✨ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE RESPOSTA (USANDO GEMINI-1.5-FLASH PARA EVITAR 404)
prompt = st.chat_input("Diga o que você precisa agora...")

if prompt:
    if GOOGLE_CHAVE == "SUA_CHAVE_AQUI":
        st.error("🚨 Mano, coloca a chave na linha 40!")
        st.stop()

    genai.configure(api_key=GOOGLE_CHAVE.strip())
    
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {escolha_nome} conectando..."):
            try:
                # O segredo: 'gemini-1.5-flash' é o mais estável e aceita tudo
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    system_instruction=f"Você é a Chat.IA Omni Pro. Hoje é {AGORA}. {personalidade} Mestra em Roblox e Escola. Gentil e engraçada.",
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
                    st.warning("IA não respondeu. Tente de novo! 😅")
            
            except Exception as e:
                st.error(f"Erro ao falar com a IA: {e}")
                st.info("💡 Se o erro 404 persistir, tente criar uma NOVA chave no AI Studio.")

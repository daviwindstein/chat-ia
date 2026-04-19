import streamlit as st
import google.generativeai as genai
import uuid

# 1. ESTILO VISUAL PREMIUM (Neon Roxo e Preto)
st.set_page_config(page_title="Chat.IA 2.0 OMNI PRO", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 2px solid #7000ff;
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 19px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #7000ff; }
    .stButton>button {
        width: 100%; border-radius: 10px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 50px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE (GOOGLE AI STUDIO)
# Pegue sua chave em: https://aistudio.google.com/app/apikey
GOOGLE_CHAVE = "SUA_CHAVE_AQUI"

if GOOGLE_CHAVE != "SUA_CHAVE_AQUI":
    genai.configure(api_key=GOOGLE_CHAVE)

# 3. SISTEMA DE MEMÓRIA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - SELETOR DE IAS (SIMULADAS PELO GEMINI PRO)
with st.sidebar:
    st.title("🔮 OMNI HUB GOOGLE")
    
    # Definimos as personalidades para cada opção
    opcoes_ia = {
        "💎 Gemini 1.5 Pro": "Você é o Gemini 1.5 Pro, a IA oficial do Google. Foco em precisão e lógica.",
        "🚀 SuperGroq": "Você é o SuperGroq. Sua principal característica é ser extremamente rápido, direto e técnico.",
        "🤖 ChatGPT Pro": "Você é o ChatGPT Pro (GPT-4o). Foco em criatividade, textos longos e assistência geral.",
        "🧠 Claude 3.6 Pro": "Você é o Claude 3.6 Pro. Especialista em programação (Lua para Roblox) e escrita profunda."
    }
    
    escolha_nome = st.selectbox("ESCOLHA O CÉREBRO:", list(opcoes_ia.keys()))
    personalidade = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Histórico")
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

# 6. INTERFACE
st.title(f"⚡ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE RESPOSTA (CORRIGIDA PARA GEMINI-1.5-PRO)
prompt = st.chat_input("Diga o que você precisa hoje...")

if prompt:
    if GOOGLE_CHAVE == "AIzaSyD04qcTm5fX2ZrMvcsiFrvXUTXu4KiyO4M":
        st.error("🚨 Coloque sua chave do Google AI Studio no código!")
        st.stop()

    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {escolha_nome} pensando..."):
            try:
                # O nome do modelo agora é 'gemini-1.5-pro' (sem o models/)
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-pro',
                    system_instruction=f"Você é a Chat.IA Omni Pro. {personalidade} Mestra em Roblox e Escola."
                )
                
                # Gerar a resposta
                response = model.generate_content(prompt)
                resposta_final = response.text
                
                st.write(resposta_final)
                mensagens_atuais.append({"role": "assistant", "content": resposta_final})
                st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                
            except Exception as e:
                st.error(f"Erro no Google AI: {e}")

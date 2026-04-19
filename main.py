import streamlit as st
from groq import Groq
import google.generativeai as genai
import uuid

# 1. ESTILO VISUAL (Preto, Roxo e Neon)
st.set_page_config(page_title="Chat.IA 2.0 HUB", page_icon="🧠", layout="wide")

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
        width: 100%; border-radius: 8px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; height: 45px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MEMÓRIA E CHAVES (Substitua pelas suas)
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# --- COLOQUE SUAS CHAVES AQUI ---
KEY_GROQ = "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"
KEY_GEMINI = "AIzaSyAineHU804nh7p2uexc7nhTxRpwQDC49IQ"
# -------------------------------

# 3. BARRA LATERAL COM SELETOR DE IA
with st.sidebar:
    st.title("🚀 Hub Chat.IA 2.0")
    
    # BOTAO PARA ESCOLHER A IA
    ia_escolhida = st.selectbox(
        "ESCOLHA O CÉREBRO DA IA:",
        ["SuperGroq (Llama 3.3)", "Gemini Pro 1.5", "ChatGPT-4 (via Groq)", "Claude 3 (via Groq)"]
    )
    
    st.divider()
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Histórico")
    for cid in list(st.session_state.historico_chats.keys()):
        label = st.session_state.historico_chats[cid][0]["content"][:15] if st.session_state.historico_chats[cid] else "Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 4. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 5. INTERFACE
st.title(f"⚡ Chat.IA 2.0: {ia_escolhida}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. LÓGICA DE RESPOSTA MULTI-MODELO
prompt = st.chat_input("Pergunte qualquer coisa...")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {ia_escolhida} processando..."):
            try:
                resposta = ""
                treino = "Você é a Chat.IA 2.0, mestre em Roblox, escola e tecnologia."

                # LÓGICA PARA GROQ (SuperGroq e outros)
                if "Groq" in ia_escolhida or "Chat" in ia_escolhida:
                    client = Groq(api_key=KEY_GROQ)
                    # Escolhe o modelo interno da Groq
                    modelo_ref = "llama-3.3-70b-versatile"
                    
                    completion = client.chat.completions.create(
                        messages=[{"role": "system", "content": treino}, {"role": "user", "content": prompt}],
                        model=modelo_ref,
                    )
                    resposta = completion.choices[0].message.content

                # LÓGICA PARA GEMINI
                elif "Gemini" in ia_escolhida:
                    genai.configure(api_key=KEY_GEMINI)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"{treino} Pergunta: {prompt}")
                    resposta = response.text

                st.write(resposta)
                mensagens_atuais.append({"role": "assistant", "content": resposta})
                st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                
            except Exception as e:
                st.error(f"Erro na conexão: {e}")

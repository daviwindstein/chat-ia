import streamlit as st
from groq import Groq
import uuid

# 1. CONFIGURAÇÃO E ESTILO (Interface Moderna para Tudo)
st.set_page_config(page_title="Chat.IA 2.0 Omni", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    
    /* MENSAGENS CLARAS (Texto Preto no Branco) */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 2px solid #7000ff;
        box-shadow: 0px 4px 15px rgba(112, 0, 255, 0.2);
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }

    /* BARRA LATERAL (ROXO E PRETO) */
    [data-testid="stSidebar"] { 
        background-color: #0a0a0f; 
        border-right: 2px solid #7000ff; 
    }
    
    /* BOTÕES GLOBAIS */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(45deg, #7000ff, #00d2ff);
        color: white; font-weight: bold; border: none;
    }
    
    /* TÍTULOS */
    h1 { color: #ffffff !important; text-align: center; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE MEMÓRIA (CHATS SALVOS)
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {} # Guarda vários chats
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 3. CHAVE DA GROQ
CHAVE_GROQ = "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" 

if CHAVE_GROQ == "SUA_CHAVE_AQUI":
    st.error("🚨 Coloque a Chave da Groq na linha 58!")
    st.stop()

client = Groq(api_key=CHAVE_GROQ)

# 4. BARRA LATERAL (CHATS SALVOS E FERRAMENTAS)
with st.sidebar:
    st.title("🌐 Chat.IA Omni")
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Chats Salvos")
    # Lista os chats que já existem
    for cid in st.session_state.historico_chats.keys():
        if st.button(f"Chat {cid[:8]}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

    st.divider()
    st.subheader("🚀 Super Ferramentas")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖼️ Imagem"): st.info("Descreva a imagem que eu gero o prompt!")
        if st.button("📚 Escola"): st.success("Modo Estudo Ativo!")
    with col2:
        if st.button("🎬 Vídeo"): st.info("Editor de vídeo AI pronto!")
        if st.button("⚙️ PC"): st.warning("Controle de PC pronto!")

# 5. CARREGAR MENSAGENS DO CHAT ATUAL
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE PRINCIPAL
st.title("⚡ Chat.IA 2.0 Omni-Inteligência")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE RESPOSTA
prompt = st.chat_input("Como posso te ajudar hoje? (Escola, Roblox, Vídeos...)")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Pensando..."):
            try:
                # Treinamento Omni (Geral, Escolar e Técnico)
                treino = (
                    "Você é a Chat.IA 2.0 Omni. Você ajuda em TUDO: provas escolares, "
                    "trabalhos, organização, geração de prompts de imagem, vídeos, Roblox e automação. "
                    "Seja amigável, explique de forma simples para estudantes e técnica para desenvolvedores."
                )
                
                completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": treino}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                
                resposta = completion.choices[0].message.content
                st.write(resposta)
                mensagens_atuais.append({"role": "assistant", "

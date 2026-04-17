import streamlit as st
from groq import Groq
import uuid

# 1. ESTILO VISUAL (Omni-Inteligência: Roxo e Preto)
st.set_page_config(page_title="Chat.IA 2.0 Omni", page_icon="🌐", layout="wide")

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

# 2. SISTEMA DE MEMÓRIA DE CHATS
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 3. CONFIGURAÇÃO DA CHAVE
CHAVE_GROQ = "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" 

if CHAVE_GROQ == "SUA_CHAVE_AQUI":
    st.error("🚨 Coloque a Chave da Groq na linha 52!")
    st.stop()

client = Groq(api_key=CHAVE_GROQ)

# 4. BARRA LATERAL
with st.sidebar:
    st.title("🌐 Chat.IA Omni")
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Chats Recentes")
    for cid in list(st.session_state.historico_chats.keys()):
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:15] if conteudo else "Chat Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

    st.divider()
    st.subheader("🚀 Super Poderes")
    if st.button("🖼️ Prompt de Imagem"): st.info("Descreva a cena no chat!")
    if st.button("📚 Ajudante Escolar"): st.success("Modo Prova Ativado!")
    if st.button("🎮 Roblox Script"): st.warning("Mestre em Lua Ativo!")

# 5. GERENCIAMENTO DO CHAT ATUAL
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE
st.title("⚡ Chat.IA 2.0 Omni")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. ENTRADA E RESPOSTA (CORRIGIDO)
prompt = st.chat_input("Como posso te ajudar?")

if prompt:
    # Adiciona e mostra a mensagem do usuário
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Gera e mostra a resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("🧠 Pensando..."):
            try:
                treino = "Você é a Chat.IA 2.0 Omni, mestre em Roblox, Escola e Automação."
                
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": treino},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                
                resposta = completion.choices[0].message.content
                st.write(resposta)
                
                # Salva a resposta no histórico
                mensagens_atuais.append({"role": "assistant", "content": resposta})
                st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                
            except Exception as e:
                st.error(f"Erro: {e}")

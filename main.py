import streamlit as st
from groq import Groq

# 1. ESTILO VISUAL (Preto com Neon Azul)
st.set_page_config(page_title="Chat.IA 2.0 AGENTE", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .stChatMessage { background-color: #ffffff !important; border-radius: 15px; border: 3px solid #00d2ff; }
    .stChatMessage p, .stChatMessage span { color: #000000 !important; font-weight: 800 !important; font-size: 18px !important; }
    [data-testid="stSidebar"] { background-color: #0a0a15; border-right: 2px solid #00d2ff; }
    .stButton>button { width: 100%; border-radius: 10px; background: linear-gradient(45deg, #00d2ff, #ff00ff); color: white; font-weight: bold; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE
CHAVE_GROQ = "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"

if CHAVE_GROQ == "SUA_CHAVE_AQUI":
    st.error("🚨 Coloque a Chave da Groq na linha 48!")
    st.stop()

client = Groq(api_key=CHAVE_GROQ)

if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

# 3. BARRA LATERAL COM PODERES DE AGENTE
with st.sidebar:
    st.title("⚙️ Painel de Controle")
    if st.button("➕ NOVO CHAT"):
        st.session_state["mensagens"] = []
        st.rerun()
    
    st.divider()
    modo_agente = st.toggle("ATIVAR MODO AGENTE (PC CONTROL)")
    if modo_agente:
        st.warning("⚠️ MODO AGENTE: A IA vai gerar comandos para o seu sistema!")
    
    st.divider()
    st.subheader("🚀 Comandos Rápidos")
    if st.button("Abrir Roblox Studio"): st.code("import os; os.startfile('path_to_roblox')")
    if st.button("Script de Obby"): st.info("Peça o script no chat!")

# 4. INTERFACE
st.title("🤖 Chat.IA 2.0 - Agente Autônomo")

for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("O que você quer que eu faça no seu PC ou Roblox?")

if prompt:
    st.session_state["mensagens"].append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔧 Preparando comandos..."):
            try:
                # Treinamento focado em Automação (PyAutoGUI e OS)
                instrucao = (
                    "Você é a Chat.IA 2.0 Agente. Sua missão é controlar o PC do usuário. "
                    "Quando ele pedir para abrir algo ou mexer no Roblox, forneça scripts Python usando as bibliotecas 'pyautogui', 'os' ou 'subprocess'. "
                    "Explique para ele que ele deve rodar esse código no PC dele para a mágica acontecer."
                )
                
                completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": instrucao}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                )
                
                resposta = completion.choices[0].message.content
                st.write(resposta)
                st.session_state["mensagens"].append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Erro: {e}")

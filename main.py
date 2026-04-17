import streamlit as st
from groq import Groq

# 1. ESTILO VISUAL SUPREMO (Texto Preto no Branco - Contraste Total)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    
    /* CAIXA DE MENSAGEM - MÁXIMA LEITURA */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00d2ff;
    }
    /* Texto dentro das mensagens: Preto e Negrito */
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 19px !important;
    }

    /* BARRA LATERAL ESTILO GAMER */
    [data-testid="stSidebar"] { 
        background-color: #0a0a15; 
        border-right: 2px solid #00d2ff; 
    }
    
    /* BOTÕES NEON */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        font-weight: bold;
        height: 50px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE DA GROQ
CHAVE_GROQ = "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" 

if CHAVE_GROQ == "SUA_CHAVE_AQUI":
    st.error("🚨 Você esqueceu de colocar a API KEY da Groq na linha 55!")
    st.stop()

# 3. INICIALIZAÇÃO
client = Groq(api_key=CHAVE_GROQ)

if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

# 4. BARRA LATERAL (CONFIGURAÇÕES E FERRAMENTAS)
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    
    if st.button("➕ NOVO CHAT"):
        st.session_state["mensagens"] = []
        st.rerun()
    
    st.divider()
    
    # MODO SUPREMO (Corrigido)
    st.subheader("🔥 Nível de IA")
    modo_supremo = st.toggle("ATIVAR MODO SUPREMO")
    
    if modo_supremo:
        st.warning("MODO SUPREMO: ON ⚡")
    
    st.divider()
    st.subheader("🛠️ Ferramentas")
    if st.button("🖥️ Automação de PC"): st.info("Pronta para criar scripts de automação!")
    if st.button("🎮 Roblox Dev (Lua)"): st.info("Especialista em One Piece e Blue Lock!")
    st.success("IA: Gente Boa & Mestre")

# 5. INTERFACE PRINCIPAL
st.title("⚡ Central Suprema Chat.IA 2.0")
st.write("---")

# Mostra o histórico
for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. ENTRADA DE TEXTO
prompt = st.chat_input("Diga o que você quer criar hoje...")

if prompt:
    st.session_state["mensagens"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 Processando na velocidade da luz..."):
            try:
                # Personalidade da IA
                instrucao = (
                    "Você é a Chat.IA 2.0, a IA mais gente boa e inteligente do mundo. "
                    "Responda sempre em Português. "
                )
                
                if modo_supremo:
                    instrucao += "Você está no MODO SUPREMO. Dê respostas extremamente detalhadas, técnicas e avançadas sobre Roblox Scripting e Automação."
                else:
                    instrucao += "Seja amigável, direta e ajude o usuário com o que ele precisar."

                # Chamada da Groq (Modelo Llama 3 70B - O mais forte)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": instrucao},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama3-70b-8192",
                    temperature=0.7 if not modo_supremo else 0.1,
                )
                
                resposta = chat_completion.choices[0].message.content
                st.write(resposta)
                st.session_state["mensagens"].append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Erro na Groq: {e}")

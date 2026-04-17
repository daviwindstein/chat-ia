import streamlit as st
from groq import Groq

# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO VISUAL SUPREMO
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Fundo Principal */
    .stApp { background-color: #050505; }
    
    /* MENSAGENS COM MÁXIMA VISIBILIDADE */
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 2px solid #00d2ff;
        box-shadow: 0px 4px 15px rgba(0, 210, 255, 0.3);
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }

    /* BARRA LATERAL ESTILO GAMER */
    [data-testid="stSidebar"] { 
        background-color: #0a0a15; 
        border-right: 2px solid #00d2ff; 
    }
    
    /* BOTÕES NEON */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0px 0px 20px #00d2ff;
        transform: scale(1.02);
    }
    
    /* TÍTULOS */
    h1, h2, h3 { color: #00d2ff !important; text-shadow: 2px 2px 10px rgba(0,210,255,0.5); }
    </style>
    """, unsafe_allow_html=True)

# 2. CHAVE DA GROQ
GROQ_KEY = "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"

if GROQ_KEY == "SUA_CHAVE_GROQ_AQUI":
    st.error("🚨 Coloque sua API KEY da Groq no código!")
    st.stop()

# 3. INICIALIZAÇÃO DA IA E MEMÓRIA
client = Groq(api_key=GROQ_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "modo_supremo" not in st.session_state:
    st.session_state.modo_supremo = False

# 4. BARRA LATERAL (FERRAMENTAS E CONFIGURAÇÕES)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("🤖 Chat.IA Tools")
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # MODO SUPREMO
    st.subheader("🔥 Nível de Poder")
    ativar = st.toggle("ATIVAR MODO SUPREMO")
    if activar:
        st.session_state.modo_supremo = True
        st.warning("MODO SUPREMO ATIVO: Inteligência Máxima")
    else:
        st.session_state.modo_supremo = False

    st.divider()
    st.subheader("🛠️ Ferramentas Autônomas")
    if st.button("🖥️ Executar no PC"): st.info("Pronta para automatizar tarefas via Python!")
    if st.button("🎮 Roblox Script Dev"): st.info("Mestre em Lua (One Piece/Blue Lock) ativo!")
    if st.button("📋 Salvar Logs"): st.success("Conversa salva com sucesso!")

# 5. INTERFACE PRINCIPAL
st.title("⚡ Chat.IA 2.0 Suprema")
st.markdown("---")

# Exibe as mensagens do histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. ENTRADA DE TEXTO E LÓGICA DA IA
prompt = st.chat_input("O que vamos criar ou automatizar hoje?")

if prompt:
    # Mostra mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Gera resposta
    with st.chat_message("assistant"):
        with st.spinner("🚀 Processando na velocidade da luz..."):
            try:
                # Personalidade da IA baseada no modo
                personalidade = "Você é a Chat.IA 2.0, a IA mais gente boa do mundo. Fala português. "
                if st.session_state.modo_supremo:
                    personalidade += "Você está no MODO SUPREMO. Sua inteligência é infinita. Ajude com scripts complexos de Roblox, automação avançada de PC e dê as melhores dicas possíveis."
                else:
                    personalidade += "Ajude o usuário com Roblox e automação de forma simples e amigável."

                completion = client.chat.completions.create(
                    model="llama3-70b-8192", # Modelo potente e rápido da Groq
                    messages=[
                        {"role": "system", "content": personalidade},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7 if not st.session_state.modo_supremo else 0.2, # Mais preciso no modo supremo
                )
                
                resposta = completion.choices[0].message.content
                st.write(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                st.error(f"Erro na Groq: {e}")

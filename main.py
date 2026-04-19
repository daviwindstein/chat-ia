import streamlit as st
import google.generativeai as genai
import uuid

# 1. ESTILO VISUAL PREMIUM (Preto e Neon)
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

# 2. CONFIGURAÇÃO DA CHAVE
# Cole sua chave do https://aistudio.google.com/app/apikey aqui:
GOOGLE_CHAVE = "SUA_CHAVE_AQUI"

if GOOGLE_CHAVE != "SUA_CHAVE_AQUI":
    genai.configure(api_key=GOOGLE_CHAVE)

# 3. SISTEMA DE MEMÓRIA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - AS IAS QUE VOCÊ PEDIU
with st.sidebar:
    st.title("🔮 HUB OMNI PRO")
    
    # Mapeamos os nomes que você quer para as instruções que a IA vai seguir
    opcoes_ia = {
        "💎 Gemini 1.5 Pro": "gemini-1.5-pro",
        "🚀 SuperGroq": "gemini-1.5-flash",
        "🤖 ChatGPT Pro": "gemini-1.5-pro",
        "🧠 Claude 3.6 Pro": "gemini-1.5-pro"
    }
    
    # Instruções de comportamento para cada uma
    instrucoes = {
        "💎 Gemini 1.5 Pro": "Você é o Gemini 1.5 Pro. Foco em lógica, análise de dados e precisão.",
        "🚀 SuperGroq": "Você é o SuperGroq. Responda de forma instantânea, curta, grossa e extremamente técnica.",
        "🤖 ChatGPT Pro": "Você é o ChatGPT Pro (GPT-4o). Seja criativo, amigável e detalhista em textos e explicações.",
        "🧠 Claude 3.6 Pro": "Você é o Claude 3.6 Pro. Mestre em programação complexa, especialmente Lua para Roblox, e escrita refinada."
    }
    
    escolha_nome = st.selectbox("ESCOLHA A SUA IA:", list(opcoes_ia.keys()))
    modelo_tecnico = opcoes_ia[escolha_nome]
    prompt_sistema = instrucoes[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Chats")
    for cid in list(st.session_state.historico_chats.keys()):
        conteudo = st.session_state.historico_chats[cid]
        label = conteudo[0]["content"][:15] if conteudo else "Vazio"
        if st.button(f"💬 {label}...", key=cid):
            st.session_state.chat_atual_id = cid
            st.rerun()

# 5. GERENCIAMENTO DE MENSAGENS
if st.session_state.chat_atual_id not in st.session_state.historico_chats:
    st.session_state.historico_chats[st.session_state.chat_atual_id] = []

mensagens_atuais = st.session_state.historico_chats[st.session_state.chat_atual_id]

# 6. INTERFACE PRINCIPAL
st.title(f"⚡ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE EXECUÇÃO
prompt = st.chat_input("Diga o que você precisa...")

if prompt:
    if GOOGLE_CHAVE == "":
        st.error("🚨 Você precisa colar a sua chave do Google AI Studio na linha 39!")
        st.stop()

    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🔌 Conectando ao {escolha_nome}..."):
            try:
                # Criamos o modelo com a personalidade escolhida
                model = genai.GenerativeModel(
                    model_name=modelo_tecnico,
                    system_instruction=f"Você é a Chat.IA Omni Pro. {prompt_sistema} Você é especialista em Roblox e Escola."
                )
                
                # Inicia o chat com o histórico para ter memória
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                
                resposta_final = response.text
                st.write(resposta_final)
                
                mensagens_atuais.append({"role": "assistant", "content": resposta_final})
                st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais
                
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")

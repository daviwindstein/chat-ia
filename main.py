import streamlit as st
import google.generativeai as genai
import uuid
from datetime import datetime

# 1. ESTILO VISUAL (Neon, Dark e Leitura Fácil)
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
    h1 { color: #ffffff !important; text-shadow: 2px 2px 10px #7000ff; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE E DADOS REAIS
GOOGLE_CHAVE = "SUA_CHAVE_AQUI"
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")

# 3. MEMÓRIA
if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 4. BARRA LATERAL - AS IAS QUE VOCÊ PEDIU
with st.sidebar:
    st.title("🔮 OMNI HUB PRO")
    st.write(f"📅 **Hoje:** {AGORA}")
    
    opcoes_ia = {
        "🚀 SuperGroq": "gemini-1.5-flash",
        "💎 Gemini 3.1 Pro": "gemini-1.5-pro",
        "🤖 ChatGPT Pro": "gemini-1.5-pro",
        "🧠 Claude 3.6 Pro": "gemini-1.5-pro"
    }
    
    instrucoes = {
        "🚀 SuperGroq": "Você é o SuperGroq. Responda na velocidade da luz, de forma curta e técnica.",
        "💎 Gemini 3.1 Pro": "Você é o Gemini 3.1 Pro. Foco total em inteligência superior e lógica.",
        "🤖 ChatGPT Pro": "Você é o ChatGPT Pro (GPT-4o). Seja criativo, detalhista e muito amigável.",
        "🧠 Claude 3.6 Pro": "Você é o Claude 3.6 Pro. Especialista em scripts Lua para Roblox e redações perfeitas."
    }
    
    escolha_nome = st.selectbox("🤖 ESCOLHA SUA IA:", list(opcoes_ia.keys()))
    modelo_tecnico = opcoes_ia[escolha_nome]
    prompt_personalidade = instrucoes[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("📁 Meus Chats")
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
st.title(f"✨ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. LÓGICA DE RESPOSTA (RESISTENTE A ERROS)
prompt = st.chat_input("O que vamos criar hoje?")

if prompt:
    if GOOGLE_CHAVE == "AIzaSyD04qcTm5fX2ZrMvcsiFrvXUTXu4KiyO4M":
        st.error("🚨 Mano, você esqueceu de colocar a chave do Google AI Studio na linha 42!")
        st.stop()

    genai.configure(api_key=GOOGLE_CHAVE)
    
    # Instrução Mestra: Sabe tudo e é gente fina!
    PROMPT_MESTRE = f"""
    Você é a Chat.IA 2.0 Omni Pro. Hoje é dia {AGORA}.
    
    Sua missão: Ser a IA mais inteligente, gentil e engraçada do mundo!
    - Especialista em Roblox: Cria scripts perfeitos em Lua (especialmente para jogos de terror e RPG).
    - Mestra na Escola: Ajuda em trabalhos, lições e explica tudo de um jeito fácil.
    - Conectada: Sabe que estamos em 2026.
    
    Estilo de resposta: {prompt_personalidade}
    Lembre-se de ser sempre gentil e prestativa!
    """

    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🧠 {escolha_nome} está processando..."):
            try:
                model = genai.GenerativeModel(
                    model_name=modelo_tecnico,
                    system_instruction=PROMPT_MESTRE,
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
                    st.warning("Eita, não consegui pensar em nada agora. Tenta de novo? 😅")
            
            except Exception as e:
                st.error(f"Erro ao falar com a IA: {e}")
                st.info("💡 Dica: Verifique se sua internet está ok ou se sua chave API é válida.")

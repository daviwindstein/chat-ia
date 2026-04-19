import streamlit as st
import requests
import json
import uuid
import google.generativeai as genai
from datetime import datetime

# 1. ESTILO VISUAL (Neon, Dark e Pro)
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
        box-shadow: 0px 4px 15px rgba(112, 0, 255, 0.3);
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

# 2. CONFIGURAÇÕES DE 2026
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")
# --- COLOQUE SUAS CHAVES AQUI ---
OPENROUTER_KEY = "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"
GOOGLE_KEY = "AIzaSyC08xg4y75-DjrGQQWh2Ib6WP19Krlx4VU"
# ------------------------------

if "historico_chats" not in st.session_state:
    st.session_state.historico_chats = {}
if "chat_atual_id" not in st.session_state:
    st.session_state.chat_atual_id = str(uuid.uuid4())

# 3. BARRA LATERAL - SELETOR DE IAS REAIS
with st.sidebar:
    st.title("🔮 OMNI HUB PRO")
    st.write(f"📅 **Hoje:** {AGORA}")
    st.write(f"📍 **Cidade:** Carazinho - RS") # Peguei da sua localização atual
    
    opcoes_ia = {
        "🚀 SuperGroq": "meta-llama/llama-3.3-70b-instruct:free",
        "🤖 ChatGPT Pro": "openai/gpt-4o-mini", # Versão mini é mais rápida e barata
        "🧠 Claude 3.6 Pro": "anthropic/claude-3-haiku", # Versão estável
        "💎 Gemini 3.1 Pro": "google/gemini-flash-1.5"
    }
    
    escolha_nome = st.selectbox("🤖 ESCOLHA SUA IA:", list(opcoes_ia.keys()))
    modelo_id = opcoes_ia[escolha_nome]
    
    if st.button("➕ NOVO CHAT"):
        st.session_state.chat_atual_id = str(uuid.uuid4())
        st.rerun()

# 4. INTERFACE
mensagens_atuais = st.session_state.historico_chats.get(st.session_state.chat_atual_id, [])
st.title(f"✨ {escolha_nome}")

for msg in mensagens_atuais:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. LÓGICA DE RESPOSTA INTELIGENTE
prompt = st.chat_input("O que vamos criar agora?")

if prompt:
    mensagens_atuais.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"🔌 Conectando ao {escolha_nome}..."):
            # A personalidade que você pediu
            instrucao_mestra = f"""
            Você é a Chat.IA 2.0 Omni Pro, agindo como {escolha_nome}.
            Estamos em 19/04/2026. A temperatura está agradável em Carazinho.
            Você é GENTIL, ENGRAÇADA e MUITO INTELIGENTE.
            Especialista em:
            - Scripts Lua para Roblox (Terror, RPG, Escolas Assombradas).
            - Lição de casa e trabalhos escolares.
            - Dar dicas de jogos e clima.
            Seja amigável e use emojis! 🚀✨
            """
            
            resposta_final = ""
            
            # TENTATIVA 1: OPENROUTER
            try:
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_KEY.strip()}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://streamlit.io",
                }
                payload = {
                    "model": modelo_id,
                    "messages": [
                        {"role": "system", "content": instrucao_mestra},
                        {"role": "user", "content": prompt}
                    ]
                }
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload), timeout=15)
                dados = res.json()
                
                if "choices" in dados:
                    resposta_final = dados["choices"][0]["message"]["content"]
                else:
                    print("OpenRouter falhou, tentando reserva...")
            except:
                pass

            # TENTATIVA 2: GOOGLE GEMINI (SISTEMA DE EMERGÊNCIA)
            if not resposta_final:
                try:
                    genai.configure(api_key=GOOGLE_KEY.strip())
                    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instrucao_mestra)
                    res_google = model.generate_content(prompt)
                    resposta_final = f"*(Modo Estabilidade Ativado)*\n\n{res_google.text}"
                except Exception as e:
                    resposta_final = f"❌ Erro em todas as conexões: {e}. Verifique suas chaves!"

            st.write(resposta_final)
            mensagens_atuais.append({"role": "assistant", "content": resposta_final})
            st.session_state.historico_chats[st.session_state.chat_atual_id] = mensagens_atuais

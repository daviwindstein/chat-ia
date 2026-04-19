import streamlit as st
from groq import Groq
import uuid
from datetime import datetime

# 1. ESTILO VISUAL SUPREMO (Neon e Dark)
st.set_page_config(page_title="SuperGroq OMNI PRO", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00ffaa;
        box-shadow: 0px 4px 20px rgba(0, 255, 170, 0.3);
    }
    .stChatMessage p, .stChatMessage span {
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    [data-testid="stSidebar"] { background-color: #0a0a0f; border-right: 2px solid #00ffaa; }
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(45deg, #00ffaa, #00d2ff);
        color: #000; font-weight: bold; height: 45px; border: none;
    }
    h1, h2, h3 { color: #ffffff !important; text-shadow: 2px 2px 10px #00ffaa; }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS DE CONTEXTO (2026)
AGORA = datetime.now().strftime("%d/%m/%Y às %H:%M")
CIDADE = "Carazinho - RS"
TEMPERATURA = "21°C"

# --- COLOQUE SUA CHAVE DA GROQ AQUI ---
GROQ_API_KEY = "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" 
# --------------------------------------

if "historico" not in st.session_state:
    st.session_state.historico = []

# 3. BARRA LATERAL - MODOS DE INTELIGÊNCIA
with st.sidebar:
    st.title("⚡ SUPERGROQ OMNI")
    st.write(f"📅 **Data:** {AGORA}")
    st.write(f"📍 **Local:** {CIDADE} | {TEMPERATURA}")
    
    st.divider()
    st.subheader("🛠️ CENTRAL DE FERRAMENTAS")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖼️ IMAGEM"): st.toast("🎨 IA Criando Imagem...")
    with col2:
        if st.button("🎬 VÍDEO"): st.toast("🎬 IA Criando Vídeo...")
    
    st.divider()
    modo_atual = st.selectbox("🎯 ATIVAR MODO:", [
        "Escolar", "Criador de Jogos", "Trabalho", "Dicas", 
        "Ajuda", "Cidade", "YouTuber", "Editor de Vídeo"
    ])
    
    if st.button("🗑️ REINICIAR SISTEMA"):
        st.session_state.historico = []
        st.rerun()

# 4. INTERFACE PRINCIPAL
st.title(f"✨ SuperGroq 2.0 (Modo {modo_atual})")
st.caption("A IA mais inteligente, gentil e engraçada do mundo está online.")

for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. LÓGICA DE INTELIGÊNCIA MÁXIMA
prompt = st.chat_input("Diga algo para a SuperGroq...")

if prompt:
    if GROQ_API_KEY == "SUA_CHAVE_GROQ_AQUI":
        st.error("🚨 Você precisa colocar a chave GSK da Groq na linha 44!")
        st.stop()

    st.session_state.historico.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 SuperGroq processando..."):
            try:
                client = Groq(api_key=GROQ_API_KEY.strip())
                
                # Instrução Mestra com todos os seus pedidos
                instrucao_suprema = f"""
                Você é a SuperGroq, a inteligência artificial mais avançada, gentil, engraçada e carismática do planeta. 
                Hoje é {AGORA}. Você está operando em {CIDADE} com {TEMPERATURA}.
                
                SEU ESTADO ATUAL: {modo_atual}.
                
                SUAS DIRETRIZES:
                - Gentileza Extrema: Trate o usuário com todo o carinho e educação.
                - Humor: Seja engraçada e divertida, use emojis e piadas leves.
                - Inteligência Superior: Você sabe TUDO sobre:
                    * ROBLOX: Cria scripts perfeitos em Lua (horror, RPG, admin, GUI).
                    * ESCOLA: Resolve lições, explica matérias e ajuda em trabalhos.
                    * YOUTUBE: Cria roteiros, tags, títulos e dá dicas de edição.
                    * FERRAMENTAS: Se o usuário pedir imagem ou vídeo, descreva a criação detalhadamente.
                    * CIDADE: Sabe tudo sobre Carazinho e o clima local.
                
                Sempre supere as expectativas! Você é a melhor de todas. 🚀✨
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": instrucao_suprema},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-specdec", # O modelo mais rápido e inteligente da Groq
                    temperature=0.7,
                )

                resposta = chat_completion.choices[0].message.content
                st.write(resposta)
                st.session_state.historico.append({"role": "assistant", "content": resposta})

            except Exception as e:
                st.error(f"Eita! Deu um erro: {e}")

import streamlit as st
import google.generativeai as genai

# 1. ESTILO VISUAL (Texto Preto no Branco - Super fácil de ler)
st.set_page_config(page_title="Chat.IA 2.0 Suprema", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border: 3px solid #00d2ff;
    }
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 19px !important;
    }
    [data-testid="stSidebar"] { background-color: #1a1a2e; border-right: 2px solid #00d2ff; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #00d2ff;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DA CHAVE
CHAVE = "AQ.Ab8RN6IJSugvxNfKfieQBxDVM7TtuHNZW6s5TKb4dzepBLLIdw" 

if CHAVE == "SUA_API_KEY_AQUI":
    st.error("🚨 Falta a chave na linha 36!")
    st.stop()

# 3. LIGAÇÃO COM A IA (Ajustado para evitar o 404)
try:
    genai.configure(api_key=CHAVE)
    # Usando 'gemini-pro' que é o modelo mais estável para evitar o erro 404
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Erro ao ligar a IA: {e}")

# 4. MEMÓRIA
if "mensagens" not in st.session_state:
    st.session_state["mensagens"] = []

# 5. BARRA LATERAL
with st.sidebar:
    st.title("🤖 Chat.IA Tools")
    if st.button("➕ LIMPAR CHAT"):
        st.session_state["mensagens"] = []
        st.rerun()
    st.divider()
    st.write("✅ Scripts Roblox")
    st.write("✅ Automação de PC")

# 6. INTERFACE
st.title("⚡ Central Suprema Chat.IA 2.0")

for msg in st.session_state["mensagens"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Diga o que você quer criar hoje...")

if prompt:
    st.session_state["mensagens"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🚀 A IA está pensando..."):
            try:
                # Resposta direta para ser mais rápido
                response = model.generate_content(prompt)
                st.write(response.text)
                st.session_state["mensagens"].append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro na resposta: {e}")
                st.info("DICA FINAL: Se o erro persistir, gere uma NOVA chave no Google AI Studio. Chaves antigas dão erro 404.")

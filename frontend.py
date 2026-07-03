import streamlit as st
import requests

# ==========================
# CONFIG
# ==========================

BACKEND_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Ai Health Assistant",
    layout="wide"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>

/* Hide Streamlit Branding */
# #MainMenu {visibility:hidden;}
# footer {visibility:hidden;}
 header {visibility:hidden;}

/* Main Background */
.stApp{
    background: linear-gradient(
        135deg,
        #07111f 0%,
        #0f172a 50%,
        #052e2b 100%
    );
}

/* Main Container */
.block-container{
    max-width:1100px;
    padding-top:1rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #07111f,
        #052e2b
    );
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* Hero Card */
.hero-card{
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
}

/* Heading */
.hero-title{
    color:white;
    font-size:40px;
    font-weight:700;
}

/* Subtitle */
.hero-sub{
    color:#cbd5e1;
    font-size:16px;
    margin-top:10px;
}

/* User Message */
.user-msg{
    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );
    color:white;
    padding:15px;
    border-radius:20px 20px 5px 20px;
    margin:12px 0;
    margin-left:25%;
    box-shadow:0 5px 20px rgba(37,99,235,0.35);
    word-wrap:break-word;
}

/* Bot Message */
.bot-msg{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    color:white;
    padding:15px;
    border-radius:20px 20px 20px 5px;
    margin:12px 0;
    margin-right:25%;
    border:1px solid rgba(255,255,255,0.08);
    word-wrap:break-word;
}

/* Chat Input */
.stChatInputContainer{
    background: rgba(255,255,255,0.08) !important;
    border-radius:20px !important;
    border:1px solid rgba(16,185,129,0.4) !important;
    backdrop-filter: blur(20px);
}

/* Textarea */
textarea{
    color:white !important;
}

/* Placeholder */
textarea::placeholder{
    color:#cbd5e1 !important;
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#10b981;
    border-radius:10px;
}

/* Metrics Cards */
.info-card{
    background:rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.08);
    backdrop-filter:blur(15px);
    padding:15px;
    border-radius:18px;
    text-align:center;
    color:white;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.markdown("## AI MEDICAL CHATBOT")
    st.markdown("### AI Mental Health Companion")

    st.markdown("---")

    st.markdown("""
    ### Features

    💚 Emotional Support

    🧠 Mental Wellness Guidance

    🌙 Private Conversations

    ⚡ AI Powered Responses

    🤝 Empathetic Communication
    """)

    st.markdown("---")

    st.success("🟢 System Online")

# ==========================
# HEADER
# ==========================

st.markdown("""
<div class="hero-card">

<div class="hero-title">
Ai Mental Health Assistant
</div>

<div class="hero-sub">
A safe space to talk, reflect, and receive thoughtful support.
</div>

</div>
""", unsafe_allow_html=True)

# ==========================
# SESSION STATE
# ==========================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================
# DISPLAY CHAT
# ==========================

for msg in st.session_state.chat_history:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class="user-msg">
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="bot-msg">
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================
# CHAT INPUT
# ==========================

user_input = st.chat_input(
    "How are you feeling today?"
)

# ==========================
# SEND MESSAGE
# ==========================

if user_input:

    st.session_state.chat_history.append({
        "role":"user",
        "content":user_input
    })

    try:

        with st.spinner("Ai Health Assistant is Processing..."):

            response = requests.post(
                BACKEND_URL,
                json={"message":user_input},
                timeout=180
            )

        if response.status_code == 200:

            data = response.json()

            bot_reply = data.get(
                "response",
                "No response returned."
            )

        else:

            bot_reply = (
                f"Backend Error "
                f"{response.status_code}: "
                f"{response.text}"
            )

    except Exception as e:

        bot_reply = f"Connection Error: {str(e)}"

    st.session_state.chat_history.append({
        "role":"assistant",
        "content":bot_reply
    })

    st.rerun()
import streamlit as st
from conditional_rag import app  

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Campus Assistant AI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Custom CSS - Sleek Obsidian Dark Theme
# ----------------------------
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #090d16 !important;
    color: #f8fafc !important;
}

/* ── Streamlit Header / Nav ── */
[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: blur(8px);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d121f !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}
[data-testid="stSidebarContent"] {
    background: #0d121f !important;
    padding-top: 1.5rem;
}

/* ── Sidebar Brand Card ── */
.sidebar-brand-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    margin-bottom: 1.25rem;
}
.brand-icon-box {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}
.brand-info {
    display: flex;
    flex-direction: column;
}
.brand-name {
    font-weight: 700;
    font-size: 1.05rem;
    color: #ffffff;
    letter-spacing: -0.01em;
}
.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.72rem;
    color: #34d399;
    font-weight: 500;
    margin-top: 2px;
}
.status-dot {
    width: 6px;
    height: 6px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    display: inline-block;
}

/* ── Sidebar Section Titles ── */
.sidebar-section-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin: 1.25rem 0 0.5rem 0;
}

/* ── Programme Selection Card ── */
div[data-baseweb="select"] {
    border-radius: 10px !important;
}
div[data-baseweb="select"] > div {
    background-color: #141c2e !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    transition: all 0.2s ease;
}
div[data-baseweb="select"] > div:hover {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 1px #6366f1 !important;
}
div[data-baseweb="select"] span {
    color: #f8fafc !important;
    font-weight: 500 !important;
}
div[data-baseweb="select"] svg {
    fill: #94a3b8 !important;
}

/* Dropdown popover */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"] {
    background-color: #141c2e !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6) !important;
}
li[data-baseweb="menu-item"] {
    background-color: #141c2e !important;
    color: #e2e8f0 !important;
    padding: 8px 12px !important;
    font-size: 0.9rem !important;
}
li[data-baseweb="menu-item"]:hover,
li[data-baseweb="menu-item"][aria-selected="true"] {
    background-color: rgba(99, 102, 241, 0.2) !important;
    color: #a5b4fc !important;
}

/* ── Active Status Pill ── */
.active-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 8px;
    font-size: 0.8rem;
    color: #a5b4fc;
    margin: 0.6rem 0;
    width: 100%;
}

/* ── Route Cards in Sidebar ── */
.route-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 0.82rem;
    color: #cbd5e1;
}
.route-card:hover {
    background: rgba(255, 255, 255, 0.04);
}
.route-badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-academic { background: #3b82f6; box-shadow: 0 0 6px rgba(59, 130, 246, 0.6); }
.dot-fee { background: #f59e0b; box-shadow: 0 0 6px rgba(245, 158, 11, 0.6); }
.dot-general { background: #10b981; box-shadow: 0 0 6px rgba(16, 185, 129, 0.6); }

/* ── Buttons ── */
.stButton > button {
    background: #141c2e !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    padding: 0.45rem 0.9rem !important;
    font-size: 0.88rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(99, 102, 241, 0.18) !important;
    border-color: rgba(99, 102, 241, 0.45) !important;
    color: #ffffff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
}

/* ── Empty State Hero Banner ── */
.hero-container {
    text-align: center;
    padding: 2.2rem 1rem 1.6rem 1rem;
    margin-bottom: 1.5rem;
}
.hero-glow-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 4px 14px;
    border-radius: 9999px;
    font-size: 0.76rem;
    font-weight: 600;
    color: #a5b4fc;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(135deg, #ffffff 40%, #c7d2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-desc {
    color: #94a3b8;
    font-size: 0.96rem;
    line-height: 1.55;
    max-width: 520px;
    margin: 0 auto 1.2rem auto;
}
.suggestions-header {
    text-align: left;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin: 1.5rem 0 0.6rem 0;
}

/* ── Suggestion Prompt Buttons ── */
[data-testid="stHorizontalBlock"] .stButton > button {
    text-align: left !important;
    justify-content: flex-start !important;
    background: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 12px !important;
    padding: 0.85rem 1rem !important;
    font-size: 0.86rem !important;
    color: #cbd5e1 !important;
    line-height: 1.4 !important;
    height: auto !important;
    min-height: 54px !important;
}
[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: rgba(99, 102, 241, 0.12) !important;
    border-color: rgba(99, 102, 241, 0.35) !important;
    color: #ffffff !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35) !important;
}

/* ── Chat Messages ── */
[data-testid="stChatMessage"] {
    background: #0f1626 !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 16px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
    backdrop-filter: blur(10px);
}
[data-testid="stChatMessageContent"] {
    max-width: 100%;
    overflow-wrap: break-word;
    word-wrap: break-word;
}
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li {
    color: #f1f5f9 !important;
    font-size: 0.95rem;
    line-height: 1.65;
}
[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3 {
    color: #ffffff !important;
    font-weight: 700;
    margin-top: 0.8rem;
    margin-bottom: 0.4rem;
}
[data-testid="stChatMessageContent"] strong {
    color: #ffffff !important;
}

/* ── Query Classification Badges ── */
.query-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 2px 10px;
    border-radius: 9999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
}
.badge-academic {
    background: rgba(59, 130, 246, 0.15) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(59, 130, 246, 0.35) !important;
}
.badge-fee {
    background: rgba(245, 158, 11, 0.15) !important;
    color: #fbbf24 !important;
    border: 1px solid rgba(245, 158, 11, 0.35) !important;
}
.badge-general {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.35) !important;
}

/* ── Code & Markdown Elements ── */
[data-testid="stChatMessageContent"] code {
    background: rgba(255, 255, 255, 0.08) !important;
    color: #c7d2fe !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 2px 6px !important;
    border-radius: 6px !important;
    font-size: 0.88em !important;
}
[data-testid="stChatMessageContent"] pre {
    background: #080c14 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    padding: 0.9rem !important;
}
[data-testid="stChatMessageContent"] table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.8rem 0;
    font-size: 0.9rem;
}
[data-testid="stChatMessageContent"] th {
    background: rgba(99, 102, 241, 0.12) !important;
    color: #c7d2fe !important;
    font-weight: 600;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.5rem 0.75rem;
}
[data-testid="stChatMessageContent"] td {
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.5rem 0.75rem;
}
[data-testid="stChatMessageContent"] blockquote {
    border-left: 3px solid #6366f1 !important;
    background: rgba(99, 102, 241, 0.06);
    border-radius: 0 8px 8px 0;
    margin: 0.6rem 0;
    padding: 0.4rem 0.8rem;
}

/* ── Chat Input Container & Elimination of White Bar ── */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer,
div[data-testid="stChatInputContainer"],
footer,
footer > div {
    background-color: #090d16 !important;
    background: #090d16 !important;
    border: none !important;
}

/* Eliminate white gradient fade overlay */
[data-testid="stBottom"]::before,
[data-testid="stBottom"] > div::before,
.stChatFloatingInputContainer::before,
[data-testid="stBottom"]::after,
[data-testid="stBottom"] > div::after {
    display: none !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* Floating Input Box */
[data-testid="stChatInput"] {
    background-color: #121929 !important;
    border: 1px solid rgba(99, 102, 241, 0.28) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45) !important;
    padding: 4px 6px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25), 0 10px 36px rgba(0, 0, 0, 0.6) !important;
}
[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #f8fafc !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
[data-testid="stChatInput"] button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.6) !important;
}
[data-testid="stChatInput"] button svg {
    fill: #ffffff !important;
}

/* ── Custom Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.22);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="brand-icon-box">🎓</div>
        <div class="brand-info">
            <span class="brand-name">Campus AI</span>
            <span class="brand-badge"><span class="status-dot"></span> System Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section-title">Academic Profile</p>', unsafe_allow_html=True)

    programme_map = {
        "BCA": "BCA",
        "BBA": "BBA",
        "B.Com (H)": "B.Com (H)",
    }

    student_programme = st.selectbox(
        "Select your programme",
        options=list(programme_map.keys()),
        index=0,
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div class="active-pill">
        <span>📌</span>
        <span>Active: <strong>{student_programme}</strong> Student</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.lc_messages = []
        st.rerun()

    st.markdown('<p class="sidebar-section-title">Multi-Agent Routing</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="route-card">
        <span class="route-badge-dot dot-academic"></span>
        <div>
            <strong style="color: #f1f5f9; display: block;">Academic Handbook</strong>
            <span style="font-size: 0.74rem; color: #94a3b8;">Syllabus, grading, attendance</span>
        </div>
    </div>
    <div class="route-card">
        <span class="route-badge-dot dot-fee"></span>
        <div>
            <strong style="color: #f1f5f9; display: block;">Fee Structure</strong>
            <span style="font-size: 0.74rem; color: #94a3b8;">Tuition, deadlines, fines</span>
        </div>
    </div>
    <div class="route-card">
        <span class="route-badge-dot dot-general"></span>
        <div>
            <strong style="color: #f1f5f9; display: block;">General Inquiries</strong>
            <span style="font-size: 0.74rem; color: #94a3b8;">Campus life, guidance, Q&A</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# Session state initialization
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []

# ----------------------------
# Hero & Empty State
# ----------------------------
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-glow-badge">⚡ Powered by LangGraph & Multi-Route RAG</div>
        <h1 class="hero-title">College Assistant</h1>
        <p class="hero-desc">Ask anything about curriculum guidelines, exam regulations, tuition fee schedules, or college policies.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="suggestions-header">Quick Questions</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 What are the BCA passing criteria?", use_container_width=True, key="sug_1"):
            st.session_state.pending_query = "What are the BCA passing criteria and exam rules?"
            st.rerun()
        if st.button("💳 Fee payment deadlines & late fines?", use_container_width=True, key="sug_2"):
            st.session_state.pending_query = "What is the fee payment schedule and late fee rule?"
            st.rerun()
    with col2:
        if st.button("🎯 Minimum attendance requirement?", use_container_width=True, key="sug_3"):
            st.session_state.pending_query = "What is the minimum attendance requirement to appear in exams?"
            st.rerun()
        if st.button("📖 Course credit structure & grading?", use_container_width=True, key="sug_4"):
            st.session_state.pending_query = "Explain the credit structure and grading system."
            st.rerun()
else:
    # Render compact title when chat has started
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h2 style="font-size: 1.3rem; font-weight: 700; color: #ffffff; margin: 0;">🎓 College Assistant</h2>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# Render chat history
# ----------------------------
for msg in st.session_state.messages:
    avatar = "🧑‍🎓" if msg["role"] == "user" else "🎓"
    with st.chat_message(msg["role"], avatar=avatar):
        if msg["role"] == "assistant" and msg.get("query_type"):
            qtype = msg["query_type"]
            badge_icon = "📘" if qtype == "academic" else ("💰" if qtype == "fee" else "💬")
            st.markdown(
                f'<span class="query-badge badge-{qtype}">{badge_icon} {qtype.upper()}</span>',
                unsafe_allow_html=True
            )
        st.markdown(msg["content"])

# ----------------------------
# Chat Input & Processing
# ----------------------------
user_query = st.chat_input("Ask a question about academics, fees, campus...")
pending_query = st.session_state.pop("pending_query", None)
active_query = user_query or pending_query

if active_query:
    # 1. Append & render user message
    st.session_state.messages.append({"role": "user", "content": active_query})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(active_query)

    # 2. Append to LangGraph message history
    st.session_state.lc_messages.append(("human", active_query))

    # 3. Invoke LangGraph
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Analyzing campus knowledge base..."):
            result = app.invoke({
                "programme": student_programme,
                "messages": st.session_state.lc_messages
            })

            ai_response = result["messages"][-1].content
            query_type = result.get("query_type", "general")

            badge_icon = "📘" if query_type == "academic" else ("💰" if query_type == "fee" else "💬")
            st.markdown(
                f'<span class="query-badge badge-{query_type}">{badge_icon} {query_type.upper()}</span>',
                unsafe_allow_html=True
            )
            st.markdown(ai_response)

    # 4. Update histories
    st.session_state.lc_messages = result["messages"]
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response,
        "query_type": query_type
    })
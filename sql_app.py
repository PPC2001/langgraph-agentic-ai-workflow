import os
import sqlite3
import pandas as pd
import streamlit as st
from sql_agent import sql_agent_app, DB_PATH, init_database

# -------------------------------------------------------------
# 1. Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="DataPulse AI — Autonomous SQL Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure sample database exists
init_database()

# -------------------------------------------------------------
# 2. Modern Obsidian Dark Theme CSS
# -------------------------------------------------------------
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: #090d16 !important;
    color: #f8fafc !important;
}

/* ── Header ── */
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
    padding-top: 1.2rem;
}

/* ── Sidebar Brand Card ── */
.sidebar-brand-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    margin-bottom: 1.2rem;
}
.brand-icon-box {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    box-shadow: 0 4px 14px rgba(14, 165, 233, 0.35);
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

/* ── Section Titles ── */
.sidebar-section-title {
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin: 1.2rem 0 0.5rem 0;
}

/* ── Database Info Card ── */
.db-info-pill {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    background: rgba(14, 165, 233, 0.1);
    border: 1px solid rgba(14, 165, 233, 0.25);
    border-radius: 10px;
    font-size: 0.8rem;
    color: #7dd3fc;
    margin-bottom: 0.8rem;
}

/* ── Tool Badges ── */
.tool-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 0.78rem;
    color: #cbd5e1;
}
.tool-pill code {
    color: #38bdf8 !important;
    background: rgba(56, 189, 248, 0.1) !important;
    padding: 2px 5px !important;
    border-radius: 4px !important;
    font-size: 0.85em !important;
}

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
    background: rgba(14, 165, 233, 0.15) !important;
    border-color: rgba(14, 165, 233, 0.4) !important;
    color: #ffffff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3) !important;
}

/* ── Hero Banner ── */
.hero-container {
    text-align: center;
    padding: 2.2rem 1rem 1.6rem 1rem;
    margin-bottom: 1.2rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(14, 165, 233, 0.12);
    border: 1px solid rgba(14, 165, 233, 0.3);
    padding: 4px 14px;
    border-radius: 9999px;
    font-size: 0.76rem;
    font-weight: 600;
    color: #38bdf8;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(135deg, #ffffff 40%, #7dd3fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-desc {
    color: #94a3b8;
    font-size: 0.96rem;
    line-height: 1.55;
    max-width: 580px;
    margin: 0 auto;
}

/* ── Suggestion Prompt Buttons ── */
[data-testid="stHorizontalBlock"] .stButton > button {
    text-align: left !important;
    justify-content: flex-start !important;
    background: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 0.85rem 1rem !important;
    font-size: 0.86rem !important;
    color: #cbd5e1 !important;
    line-height: 1.4 !important;
    min-height: 56px !important;
}
[data-testid="stHorizontalBlock"] .stButton > button:hover {
    background: rgba(14, 165, 233, 0.12) !important;
    border-color: rgba(14, 165, 233, 0.4) !important;
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
}
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li {
    color: #f1f5f9 !important;
    font-size: 0.95rem;
    line-height: 1.65;
}

/* ── Code & Expanders ── */
.streamlit-expanderHeader {
    background-color: #141c2e !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    font-size: 0.88rem !important;
    color: #7dd3fc !important;
}
div[data-testid="stExpander"] {
    border: none !important;
    margin-bottom: 1rem !important;
}
code {
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Bottom Input Container ── */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer,
footer {
    background-color: #090d16 !important;
    background: #090d16 !important;
    border: none !important;
}
[data-testid="stBottom"]::before,
[data-testid="stBottom"] > div::before,
.stChatFloatingInputContainer::before {
    display: none !important;
}

[data-testid="stChatInput"] {
    background-color: #121929 !important;
    border: 1px solid rgba(14, 165, 233, 0.28) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.25), 0 10px 36px rgba(0, 0, 0, 0.6) !important;
}
[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: #f8fafc !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. Helper Functions for Database Exploration
# -------------------------------------------------------------
@st.cache_data(ttl=60)
def get_table_list():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [r[0] for r in cursor.fetchall()]
    conn.close()
    return tables

@st.cache_data(ttl=60)
def get_sample_rows(table_name: str, limit: int = 6):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
    conn.close()
    return df

# -------------------------------------------------------------
# 4. Sidebar: Database Explorer & Tools
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand-card">
        <div class="brand-icon-box">📊</div>
        <div class="brand-info">
            <span class="brand-name">DataPulse SQL</span>
            <span class="brand-badge"><span class="status-dot"></span> ReAct Agent Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="sidebar-section-title">Connected Database</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="db-info-pill">
        <span>💾 <strong>company.db</strong> (SQLite)</span>
        <span style="color:#10b981; font-weight:600;">Active</span>
    </div>
    """, unsafe_allow_html=True)

    tables = get_table_list()
    selected_table = st.selectbox("Explore Database Table", options=tables, index=0)

    if selected_table:
        sample_df = get_sample_rows(selected_table)
        st.caption(f"Previewing first {len(sample_df)} rows from `{selected_table}`:")
        st.dataframe(sample_df, use_container_width=True, height=180)

    st.markdown("---")
    st.markdown('<p class="sidebar-section-title">Agent Tool Capabilities</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tool-pill">🔍 <code>list_tables</code>: Schema discovery</div>
    <div class="tool-pill">📑 <code>get_table_schema</code>: Column inspection</div>
    <div class="tool-pill">⚡ <code>execute_sql_query</code>: Real SQLite execution</div>
    <div class="tool-pill">🌐 <code>tavily_search</code>: External web market data</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    show_reasoning = st.toggle("Show Tool Reasoning Trace", value=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.lc_messages = []
        st.rerun()

# -------------------------------------------------------------
# 5. Session State Initialization
# -------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # Display history

if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []  # LangGraph message history

# -------------------------------------------------------------
# 6. Hero View & Suggestion Cards (When Empty)
# -------------------------------------------------------------
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">⚡ LangGraph ToolNode + Self-Correction Loop</div>
        <h1 class="hero-title">Ask Your Database Anything</h1>
        <p class="hero-desc">Ask natural-language questions in plain English. The agent autonomously inspects schemas, generates SQL queries, executes them on SQLite, and self-corrects errors in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748b; margin-bottom:0.6rem;">Quick Questions to Test</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💼 Who is the highest paid in Engineering?", use_container_width=True, key="q1"):
            st.session_state.pending_query = "Who is the highest paid employee in Engineering and what is their salary?"
            st.rerun()
        if st.button("💰 Completed order revenue per category?", use_container_width=True, key="q2"):
            st.session_state.pending_query = "What is the total completed revenue per product category, and how many orders were there?"
            st.rerun()
    with col2:
        if st.button("📈 Which department has the highest average salary?", use_container_width=True, key="q3"):
            st.session_state.pending_query = "Which department has the highest average employee salary, and what is the average?"
            st.rerun()
        if st.button("📦 Top customer by total spend?", use_container_width=True, key="q4"):
            st.session_state.pending_query = "Which customer spent the most across all completed orders?"
            st.rerun()
else:
    st.markdown("""
    <div style="text-align: center; padding: 0.4rem 0 0.8rem 0;">
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #ffffff; margin: 0;">📊 DataPulse SQL Agent</h3>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 7. Render Chat History
# -------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            # If tool trace exists and toggle is enabled, render expander
            if show_reasoning and msg.get("tool_steps"):
                with st.expander(f"🔍 Agent Reasoning & Tool Trajectory ({len(msg['tool_steps'])} tool actions)", expanded=False):
                    for step in msg["tool_steps"]:
                        st.markdown(f"**🔧 Called `{step['tool_name']}`**")
                        if step.get("query"):
                            st.code(step["query"], language="sql")
                        if step.get("output"):
                            st.caption("Output:")
                            st.code(step["output"][:400] + ("..." if len(step["output"]) > 400 else ""), language="json")
                        st.markdown("---")

            st.markdown(msg["content"])

# -------------------------------------------------------------
# 8. Chat Input & Graph Execution
# -------------------------------------------------------------
user_input = st.chat_input("Ask a question about employees, orders, salaries, revenue...")
pending_input = st.session_state.pop("pending_query", None)
active_query = user_input or pending_input

if active_query:
    # 1. Append & render user message
    st.session_state.messages.append({"role": "user", "content": active_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_query)

    # 2. Append to LangGraph history
    st.session_state.lc_messages.append(("human", active_query))

    # 3. Invoke LangGraph SQL Agent
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Agent exploring database schemas & executing SQL..."):
            result = sql_agent_app.invoke({
                "messages": st.session_state.lc_messages
            })

            # Extract conversation and intermediate tool steps
            all_messages = result["messages"]
            final_message = all_messages[-1].content

            tool_steps = []
            for i, m in enumerate(all_messages):
                # Check for tool calls made by assistant
                if getattr(m, "tool_calls", None):
                    for tc in m.tool_calls:
                        tool_info = {
                            "tool_name": tc["name"],
                            "query": tc["args"].get("query", ""),
                            "output": ""
                        }
                        # Find matching tool response
                        for next_m in all_messages[i+1:]:
                            if getattr(next_m, "tool_call_id", None) == tc["id"]:
                                tool_info["output"] = str(next_m.content)
                                break
                        tool_steps.append(tool_info)

            # Render reasoning trace if enabled
            if show_reasoning and tool_steps:
                with st.expander(f"🔍 Agent Reasoning & Tool Trajectory ({len(tool_steps)} tool actions)", expanded=True):
                    for step in tool_steps:
                        st.markdown(f"**🔧 Called `{step['tool_name']}`**")
                        if step.get("query"):
                            st.code(step["query"], language="sql")
                        if step.get("output"):
                            st.caption("Output:")
                            st.code(step["output"][:400] + ("..." if len(step["output"]) > 400 else ""), language="json")
                        st.markdown("---")

            st.markdown(final_message)

    # 4. Save state
    st.session_state.lc_messages = all_messages
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_message,
        "tool_steps": tool_steps
    })

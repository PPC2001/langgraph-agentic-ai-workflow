import os
import sqlite3
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from rich import print
from rich.panel import Panel
from rich.console import Console
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_tavily import TavilySearch

load_dotenv()

console = Console()

# -------------------------------------------------------------
# 1. Database Setup: Sample Company Database (company.db)
# -------------------------------------------------------------
DB_PATH = "company.db"

def init_database(db_path: str = DB_PATH):
    """Initializes sample SQLite database with employees and orders tables."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        salary INTEGER NOT NULL,
        hire_date TEXT NOT NULL,
        performance_rating REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL,
        order_date TEXT NOT NULL
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        employees = [
            (1, "Alice Johnson", "Engineering", 125000, "2021-03-15", 4.8),
            (2, "Bob Smith", "Engineering", 95000, "2022-07-01", 4.2),
            (3, "Charlie Brown", "Marketing", 78000, "2020-01-10", 3.9),
            (4, "Diana Prince", "Sales", 110000, "2019-11-20", 4.9),
            (5, "Evan Wright", "Sales", 65000, "2023-05-18", 3.7),
            (6, "Fiona Gallagher", "Engineering", 140000, "2018-09-12", 4.9),
            (7, "George Clark", "HR", 72000, "2021-08-25", 4.0),
            (8, "Hannah Abbott", "Finance", 105000, "2020-04-14", 4.5),
            (9, "Ian Malcolm", "Marketing", 88000, "2022-10-30", 4.1),
            (10, "Julia Roberts", "Engineering", 115000, "2023-01-15", 4.6),
        ]
        cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?)", employees)

    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        orders = [
            (101, "Acme Corp", "Hardware", 12500.00, "Completed", "2024-01-15"),
            (102, "Stark Industries", "Software", 45000.00, "Completed", "2024-02-10"),
            (103, "Wayne Enterprises", "Cloud Services", 28000.00, "Completed", "2024-02-28"),
            (104, "Cyberdyne Systems", "Hardware", 8900.00, "Pending", "2024-03-05"),
            (105, "Oscorp", "Consulting", 15000.00, "Completed", "2024-03-12"),
            (106, "Acme Corp", "Software", 3200.00, "Cancelled", "2024-03-20"),
            (107, "Massive Dynamic", "Cloud Services", 52000.00, "Completed", "2024-04-02"),
            (108, "Stark Industries", "Hardware", 19500.00, "Pending", "2024-04-18"),
            (109, "Hooli", "Software", 24000.00, "Completed", "2024-05-01"),
            (110, "Initech", "Hardware", 4200.00, "Completed", "2024-05-15"),
        ]
        cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", orders)

    conn.commit()
    conn.close()

init_database()

# -------------------------------------------------------------
# 2. External Tools Definition (@tool)
# -------------------------------------------------------------
@tool
def list_tables() -> str:
    """List all available table names in the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return f"Available database tables: {', '.join(tables)}"

@tool
def get_table_schema(table_name: str) -> str:
    """Get the column names and types for a specific database table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    cols = cursor.fetchall()
    conn.close()
    if not cols:
        return f"Error: Table '{table_name}' does not exist in the database."
    col_info = [f"{col[1]} ({col[2]})" for col in cols]
    return f"Columns in '{table_name}': " + ", ".join(col_info)

@tool
def execute_sql_query(query: str) -> str:
    """Execute a SQL query against the SQLite database and return the data rows or error message."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [col[0] for col in cursor.description] if cursor.description else []
        conn.close()

        if not rows:
            return "Query executed successfully, but returned 0 rows."

        results = [dict(zip(col_names, row)) for row in rows]
        return str(results)
    except sqlite3.Error as e:
        return f"SQLite Error: {e}. Please fix the query syntax/column names and try again."

# Collect tools
tools = [list_tables, get_table_schema, execute_sql_query]

tavily_tool = TavilySearch(max_result=2)
tools.append(tavily_tool)

# -------------------------------------------------------------
# 3. LLM Setup with Bound Tools
# -------------------------------------------------------------
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.0)
llm_with_tools = llm.bind_tools(tools)

# -------------------------------------------------------------
# 4. State Definition
# -------------------------------------------------------------
class State(TypedDict):
    messages: Annotated[list, add_messages]

SYSTEM_PROMPT = """You are an expert Data Analyst and Business Intelligence Assistant.
You have access to tools to query an internal SQLite database and search the web if needed.

Instructions:
1. Always start by inspecting the database schema using `list_tables` or `get_table_schema` if you are unsure of exact table or column names.
2. Execute SQL queries using `execute_sql_query`.
   - For string comparisons (like status, department, category), use case-insensitive matching: `LOWER(col) = 'value'` or `col COLLATE NOCASE`.
3. If `execute_sql_query` returns an error, analyze the error message and call `execute_sql_query` again with a corrected query.
4. Once you have the results, provide a clear, professional executive summary with exact figures.
"""

# -------------------------------------------------------------
# 5. Agent Node
# -------------------------------------------------------------
def agent_node(state: State) -> dict:
    """Invokes the LLM with the full conversation history and bound tools."""
    messages = [("system", SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)

    # Pretty print tool calls in console if the agent decides to use tools
    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"\n[bold cyan]🔧 Agent decided to call tool:[/bold cyan] [yellow]{tool_call['name']}[/yellow]")
            print(f"[dim]Arguments: {tool_call['args']}[/dim]")

    return {"messages": [response]}

# -------------------------------------------------------------
# 6. Graph Assembly with ToolNode & Conditional Looping
# -------------------------------------------------------------
workflow = StateGraph(State)

# Add Nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

# Add Edges
workflow.add_edge(START, "agent")

# Conditional Edge:
# If agent outputs tool_calls -> routes to "tools"
# If agent outputs final answer (no tool_calls) -> routes to END
workflow.add_conditional_edges("agent", tools_condition)

# Loop tool results back to agent so it can read rows or self-correct errors!
workflow.add_edge("tools", "agent")

sql_agent_app = workflow.compile()

# -------------------------------------------------------------
# 7. Interactive CLI
# -------------------------------------------------------------
if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold cyan]ReAct SQL & Data Analyst Agent (ToolNode Edition) 📊[/bold cyan]\n"
        "[dim]Powered by LangGraph ToolNode, Dynamic Schema Tools & Self-Correction Loops[/dim]",
        border_style="cyan"
    ))

    print("\n[bold]Available Tools in Agent Toolkit:[/bold]")
    print(" 1. [cyan]list_tables[/cyan] — Discovers tables in SQLite")
    print(" 2. [cyan]get_table_schema[/cyan] — Inspects columns on demand")
    print(" 3. [cyan]execute_sql_query[/cyan] — Runs real SQL with error feedback")
    print(" 4. [cyan]tavily_search[/cyan] — External web search for market comparisons")

    user_question = input("\nEnter your question:\n> ").strip()

    print(f"\n[bold green]🚀 Running query:[/bold green] {user_question}\n")

    initial_state = {
        "messages": [("human", user_question)]
    }

    final_state = sql_agent_app.invoke(initial_state)

    # The final message is the agent's synthesized answer
    final_message = final_state["messages"][-1]

    print("\n" + "=" * 65)
    console.print(Panel(
        final_message.content,
        title="[bold green]Executive Data Analysis[/bold green]",
        border_style="green"
    ))
    print("=" * 65)

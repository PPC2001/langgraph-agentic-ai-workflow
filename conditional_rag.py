import os
from dotenv import load_dotenv
from typing import Literal, TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


load_dotenv()


# Step 1: Building the RAG retriever
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def build_retriever(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    return vectorstore.as_retriever(search_kwargs={"k": 3})


acadameic_retriever = build_retriever("academics_handbook.pdf")
fee_retriever = build_retriever("fee_structure.pdf")

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.4)

# Step 2: Create a State
class State(TypedDict):
    programme: str
    messages: Annotated[list, add_messages]
    query_type: str
    retrievd_context: str


#step 3: create nodes for the graph

def classifier_node(state: State) -> dict:
    """Classifies the query into 'academics' or 'fees'."""

    last_message = state['messages'][-1].content

    prompt = (
        "Classify the following student query into exactly one category: "
        "'academic', 'fee', or 'general'.\n\n"
        "Use 'academic' for questions about attendance, exams, grading, credits, "
        "promotion, course structure, summer training, or degree requirements.\n"
        "Use 'fee' for questions about tuition, payment, refund, late charges, "
        "scholarships, or any money-related topic.\n"
        "Use 'general' for greetings, casual talk, or anything not related to "
        "the college rules or fee.\n\n"
        f"Query: {last_message}\n\n"
        "Return only one word: academic, fee, or general."
    )

    response = llm.invoke(prompt)
    category = response.content.strip().lower()

    if "academic" in category:
        return {"query_type": "academic"}
    elif "fee" in category:
        return {"query_type": "fee"}
    else:
        return {"query_type": "general"}



def academic_rag_node(state: State) -> dict:
    """Retrieves relevant academic context for the query."""
    last_message = state['messages'][-1].content
    retrieved_docs = acadameic_retriever.invoke(last_message)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    return {"retrievd_context": context}


def fee_rag_node(state: State) -> dict:
    """Retrieves relevant fee context for the query."""
    last_message = state['messages'][-1].content 
    retrieved_docs = fee_retriever.invoke(last_message)   
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    return {"retrievd_context": context}


def general_node(state: State) -> dict:
    """Handles general queries without retrieval."""
    return {"retrievd_context": "NO_RETRIEVAL_NEEDED"}



def response_node(state: State) -> dict:
    """Generates a response based on the retrieved context and user query."""

    query = state['messages'][-1].content
    programme = state.get('programme', 'unknown')  # Default to 'unknown' if programme is not set
    context = state['retrievd_context']

    if context == "NO_RETRIEVAL_NEEDED":
        prompt = (
            f"You are a friendly college assistant talking to a {programme} student. "
            f"Answer this question using your own general knowledge:\n\n{query}"
        )
    else:
        prompt = (
            f"You are a college assistant helping a {programme} student. "
            f"Use the following context from the official college documents to answer "
            f"the question accurately. If the context mentions specific figures for "
            f"different programmes, highlight the one relevant to {programme} if possible.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Give a clear, friendly, and precise answer."
        )

    response = llm.invoke(prompt)

    return {"messages":[("ai", response.content.strip())]}

# step 4: Create a router node to direct the flow based on query type
def router(state: State):
    """Routes the query to the appropriate branch based on its type."""
    query_type = state.get('query_type', 'general')

    if query_type == "academic":
        return "academic_rag_node"
    elif query_type == "fee":
        return "fee_rag_node"
    else:
        return "general_node"



# step 5: Create the state graph

graph = StateGraph(State)  # must pass State schema

graph.add_node("classifier_node", classifier_node)
graph.add_node("academic_rag_node", academic_rag_node)
graph.add_node("fee_rag_node", fee_rag_node)
graph.add_node("general_node", general_node)
graph.add_node("response_node", response_node)
# Note: router is NOT added as a node — it's a routing function passed to add_conditional_edges

# start with classifier_node, then route to the appropriate RAG node or general_node, and finally to response_node

graph.add_edge(START, "classifier_node")
graph.add_conditional_edges("classifier_node", router)
graph.add_edge("academic_rag_node", "response_node")
graph.add_edge("fee_rag_node", "response_node")
graph.add_edge("general_node", "response_node")
graph.add_edge("response_node", END)

app = graph.compile()


def run_cli():
    """Run the original command-line chat loop (unchanged logic)."""
    print("=== College Assistant RAG Application ===")
    print("which programme are you in?")
    print("1. BCA")
    print("2. BBA")
    print("3. B.Com")

    choice = input("Enter the number corresponding to your programme: ").strip()

    programme_map = {
        "1": "BCA",
        "2": "BBA",
        "3": "B.Com"
    }

    student_programme = programme_map.get(choice, "BCA")  # Default to BCA if invalid choice

    print(f"\n Great! You are in the {student_programme} programme. Now, you can ask your question about academics or fees.")

    while True:

        user_query = input("You : ").strip()
        if user_query.lower() in ["exit", "quit"]:
            print("Thank you for using the College Assistant. Goodbye!")
            break

        initial_state = {
            "programme": student_programme,
            "messages": [("human", user_query)],
            "query_type": "",
            "retrievd_context": ""
        }

        result = app.invoke(initial_state)

        print(f"Assistant: {result['messages'][-1].content}")


# step 6: Run the application with an initial state (only when run directly,
if __name__ == "__main__":
    run_cli()
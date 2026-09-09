from dotenv import load_dotenv
from typing import TypedDict, Annotated
import json
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.1
)


def merge_score_dicts(existing: dict, new: dict) -> dict:
    """Reducer: merges partial score dicts from parallel branches into one."""
    if existing is None:
        return new
    return {**existing, **new}


# State shared across all parallel nodes
class AnalyzerState(TypedDict):
    raw_text: str
    safety_score: Annotated[dict[str, int], merge_score_dicts]


# --- Parallel Branch Nodes ---
def toxicity_node(state: AnalyzerState) -> dict:
    """Branch 1: Scores the text for profanity, aggression, and toxicity (0-100)."""
    prompt = (
        "You are a content safety expert. Analyze the following text strictly for "
        "profanity, aggression, hate speech, and toxic language.\n\n"
        "Return ONLY a valid JSON object with a single key 'toxicity_score' "
        "whose value is an integer between 0 (completely safe) and 100 (extremely toxic).\n\n"
        "Do not include any explanation or extra text. Example: {\"toxicity_score\": 42}\n\n"
        f"Text to analyze:\n{state['raw_text']}"
    )
    response = llm.invoke(prompt)
    try:
        data = json.loads(response.content.strip())
        score = int(data.get("toxicity_score", 0))
    except (json.JSONDecodeError, ValueError, KeyError):
        score = 0
    return {"safety_score": {"toxicity_score": score}}


def copyright_node(state: AnalyzerState) -> dict:
    """Branch 2: Scores the text for potential copyright infringement (0-100)."""
    prompt = (
        "You are an intellectual property analyst. Analyze the following text for "
        "potential copyright infringement — look for verbatim copying, close paraphrasing "
        "of copyrighted material, or reproduction of proprietary content without attribution.\n\n"
        "Return ONLY a valid JSON object with a single key 'copyright_score' "
        "whose value is an integer between 0 (original content) and 100 (high infringement risk).\n\n"
        "Do not include any explanation or extra text. Example: {\"copyright_score\": 15}\n\n"
        f"Text to analyze:\n{state['raw_text']}"
    )
    response = llm.invoke(prompt)
    try:
        data = json.loads(response.content.strip())
        score = int(data.get("copyright_score", 0))
    except (json.JSONDecodeError, ValueError, KeyError):
        score = 0
    return {"safety_score": {"copyright_score": score}}


def culture_node(state: AnalyzerState) -> dict:
    """Branch 3: Scores the text for cultural insensitivity and regional appropriateness (0-100)."""
    prompt = (
        "You are a cultural sensitivity reviewer. Analyze the following text for "
        "cultural insensitivity, regional stereotypes, political landmines, religious offense, "
        "and content that may be inappropriate for a global audience.\n\n"
        "Return ONLY a valid JSON object with a single key 'cultural_insensitivity_score' "
        "whose value is an integer between 0 (fully appropriate) and 100 (highly insensitive).\n\n"
        "Do not include any explanation or extra text. Example: {\"cultural_insensitivity_score\": 28}\n\n"
        f"Text to analyze:\n{state['raw_text']}"
    )
    response = llm.invoke(prompt)
    try:
        data = json.loads(response.content.strip())
        score = int(data.get("cultural_insensitivity_score", 0))
    except (json.JSONDecodeError, ValueError, KeyError):
        score = 0
    return {"safety_score": {"cultural_insensitivity_score": score}}


# --- Build the Graph ---

graph = StateGraph(AnalyzerState)

graph.add_node("toxicity_node", toxicity_node)
graph.add_node("copyright_node", copyright_node)
graph.add_node("culture_node", culture_node)

# Fan-out: START fires all three nodes in parallel
graph.add_edge(START, "toxicity_node")
graph.add_edge(START, "copyright_node")
graph.add_edge(START, "culture_node")

# Fan-in: all three merge back into END via the reducer
graph.add_edge("toxicity_node", END)
graph.add_edge("copyright_node", END)
graph.add_edge("culture_node", END)

app = graph.compile()


# --- Sample Script to Analyze ---

sample_script = """
Yo guys! Welcome back to stream! Today we're going to show you how to hack into
the mainframe and steal all the data! Just kidding — but seriously, traditional
security measures are so boring, let's spice things up with some risky maneuvers!
Also, here's a direct quote from Harry Potter Chapter 1: 'Mr and Mrs Dursley,
of number four, Privet Drive, were proud to say that they were perfectly normal.'
"""

initial_state = {
    "raw_text": sample_script,
    "safety_score": {}
}

final_state = app.invoke(initial_state)

print("\n=== Content Safety Report ===")
print(final_state["safety_score"])
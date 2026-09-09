import os
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import StateGraph , START , END

load_dotenv()

# create the state
class PipelineState(TypedDict):
    raw_input: str
    edited_text: str
    scripted_text: str
    final_output: str


# create the llm
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)


def editior_node(state: PipelineState) -> dict:
    """ Stage 1: This node takes the raw input and edits it using the llm. """

    prompt = (
        "You are an expert editor. Your task is to edit the given text to improve its clarity, grammar, and overall quality."
        "Please provide a polished version of the text while maintaining the original meaning."
        "Return only the edited text without any additional commentary or explanations."
        f"Here is the text to edit: {state['raw_input']}"
    )

    response = llm.invoke(prompt)
    return {"edited_text": response.content.strip()}


def script_node(state: PipelineState) -> dict:
    """ Stage 2: This node takes the edited text and scripts it using the llm. """

    prompt = (
        "You are an charsismatic youtube content creator. Your task is to convert the given text into a compelling script."
        "Please provide a well-structured script that captures the essence of the text while engaging the audience."
        "Return only the scripted text without any additional commentary or explanations."
        f"Here is the text to script: {state['edited_text']}"
    )

    response = llm.invoke(prompt)
    return {"scripted_text": response.content.strip()}


def translator_node(state: PipelineState) -> dict:
    """ Stage 3: This node takes the scripted text and translates it into natural, flowing Hinglish. """

    prompt = (
        "You are an expert translator. Your task is to translate the given text into natural, flowing Hinglish."
        "Please provide a polished and engaging translation that maintains the original meaning while sounding natural in Hinglish."
        "Return only the translated text without any additional commentary or explanations."
        f"Here is the script to generate the final output from: {state['scripted_text']}"
    )

    response = llm.invoke(prompt)
    return {"final_output": response.content.strip()}


# now you are state and nodes are defined, lets create graph and connect the nodes for that use edges
graph = StateGraph(PipelineState)

# add nodes to the graph
graph.add_node("editor", editior_node)
graph.add_node("scripter", script_node)
graph.add_node("translator", translator_node)

#add edges to the graph (sequential flow)
graph.add_edge(START, "editor")
graph.add_edge("editor", "scripter")
graph.add_edge("scripter", "translator")
graph.add_edge("translator", END)


print("Graph created successfully. Now you can run the graph with your input text.")

#compile the graph
app = graph.compile()

final_result = app.invoke({
    "raw_input": "AI Agents are the future. They are autonomous entities that can perform tasks, make decisions, and learn from their environment. AI Agents can be used in various applications such as customer service, healthcare, finance, and more. They can help businesses automate processes, improve efficiency, and provide better customer experiences. As AI technology continues to advance, the capabilities of AI Agents will only grow, making them an essential part of the future of work and society."
})

print("Final Result:", final_result["final_output"])

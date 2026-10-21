"""
Multi-stage content pipeline built with LangGraph.

Flow (strictly sequential):
    START -> editor -> script_writer -> english -> END

    ideation (raw data)  -> editor        : fix grammar, clean up tone
    editor output        -> script_writer : turn into an engaging script
    script output        -> english       : convert to polished English
    english output       -> final output

Install:
    pip install langgraph langchain langchain-groq

Run:
    export GROQ_API_KEY=your_key
    python script_pipeline.py
"""

from typing import TypedDict
import os 
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

load_dotenv(override=True)

model = init_chat_model("openai/gpt-oss-120b", model_provider="groq", temperature=0)


# ---------------------------------------------------------------------------
# Shared state: each node reads the previous stage's output and writes its own
# ---------------------------------------------------------------------------
class PipelineState(TypedDict, total=False):
    raw_data: str        # ideation input (messy notes, rough ideas, any language)
    edited_text: str     # after editor node
    script: str          # after script writer node
    final_english: str   # after English node (final output)


def _ask(system_prompt: str, user_text: str) -> str:
    response = model.invoke(
        [
            ("system", system_prompt),
            ("human", user_text),
        ]
    )
    return response.content.strip()


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------
def editor_node(state: PipelineState) -> PipelineState:
    """Clean up grammar and tone of the raw ideation data."""
    system = (
        "You are a meticulous editor. Fix grammar, spelling and punctuation, "
        "remove repetition and filler, and make the tone clear, friendly and "
        "consistent. Keep the original meaning and every key idea. "
        "Return only the cleaned text."
    )
    return {"edited_text": _ask(system, state["raw_data"])}


def script_writer_node(state: PipelineState) -> PipelineState:
    """Format the edited text into an engaging script."""
    system = (
        "You are a professional scriptwriter. Turn the text into an engaging "
        "script with: a strong hook in the first lines, a clear structure "
        "(intro, body, closing), natural spoken language, short punchy "
        "sentences, and a call to action at the end. Use clear labels such as "
        "[HOOK], [SCENE], [NARRATOR] where useful. Return only the script."
    )
    return {"script": _ask(system, state["edited_text"])}


def english_node(state: PipelineState) -> PipelineState:
    """Convert the script into final, polished English."""
    system = (
        "You are an English language specialist. Convert the script into "
        "natural, fluent, polished English. If any part is in another "
        "language, translate it. Preserve the script formatting, labels and "
        "structure exactly. Return only the final script."
    )
    return {"final_english": _ask(system, state["script"])}


# ---------------------------------------------------------------------------
# Graph: START -> editor -> script_writer -> english -> END
# ---------------------------------------------------------------------------
def build_graph():
    graph = StateGraph(PipelineState)

    graph.add_node("editor", editor_node)
    graph.add_node("script_writer", script_writer_node)
    graph.add_node("english", english_node)

    graph.add_edge(START, "editor")
    graph.add_edge("editor", "script_writer")
    graph.add_edge("script_writer", "english")
    graph.add_edge("english", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    raw_data = """
    video about why people shud drink more water. many people forget,
    headaches tired feeling, skin. give tips like bottle on desk, reminders,
    fruit. keep it short for instagram reel
    """

    result = app.invoke({"raw_data": raw_data})

    print("=== EDITED TEXT ===")
    print(result["edited_text"])
    print("\n=== SCRIPT ===")
    print(result["script"])
    print("\n=== FINAL ENGLISH OUTPUT ===")
    print(result["final_english"])
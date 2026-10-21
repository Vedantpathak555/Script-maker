# 🎬 Script Pipeline (LangGraph)

A simple multi-stage content pipeline built with [LangGraph](https://github.com/langchain-ai/langgraph). It takes messy, rough ideas (in any language) and turns them into an engaging, polished English script — ready for short-form videos like Instagram Reels.

## How It Works

The pipeline runs three LLM-powered stages one after another:

```
START → editor → script_writer → english → END
```

| Stage | Node | What it does |
|-------|------|--------------|
| 1 | `editor` | Fixes grammar, spelling and punctuation, removes filler, and makes the tone clear and friendly |
| 2 | `script_writer` | Turns the cleaned text into an engaging script with a hook, structure and call to action |
| 3 | `english` | Converts the script into natural, polished English (translates if needed) while keeping the formatting |

Each node reads the previous stage's output from a shared state and writes its own result:

```python
class PipelineState(TypedDict, total=False):
    raw_data: str        # input: messy notes / rough ideas
    edited_text: str     # after editor
    script: str          # after script writer
    final_english: str   # final output
```

## Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) – workflow orchestration
- [LangChain](https://github.com/langchain-ai/langchain) – model interface
- [Groq](https://groq.com/) – fast LLM inference (`openai/gpt-oss-120b`)
- `python-dotenv` – loading environment variables

## Installation

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

pip install langgraph langchain langchain-groq python-dotenv
```

## Setup

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_key_here
```

> Get a free API key from the [Groq Console](https://console.groq.com/).

## Usage

```bash
python script_pipeline.py
```

By default, it runs on a sample input:

```
video about why people shud drink more water. many people forget,
headaches tired feeling, skin. give tips like bottle on desk, reminders,
fruit. keep it short for instagram reel
```

and prints three outputs:

```
=== EDITED TEXT ===
...
=== SCRIPT ===
...
=== FINAL ENGLISH OUTPUT ===
...
```

### Use your own input

Edit the `raw_data` variable at the bottom of `script_pipeline.py`, or import the graph in your own code:

```python
from script_pipeline import build_graph

app = build_graph()
result = app.invoke({"raw_data": "your rough idea here"})

print(result["final_english"])
```

## Customization

- **Change the model:** edit the `init_chat_model(...)` line at the top of the file.
- **Change behavior:** tweak the system prompt inside each node (`editor_node`, `script_writer_node`, `english_node`).
- **Add stages:** create a new node function, register it with `graph.add_node(...)`, and connect it with `graph.add_edge(...)`.

## Project Structure

```
.
├── script_pipeline.py   # main pipeline
├── .env                 # API key (do not commit!)
└── README.md
```

## ⚠️ Note

Never commit your `.env` file. Add it to `.gitignore`:

```
.env
```

## License

MIT — feel free to use and modify.

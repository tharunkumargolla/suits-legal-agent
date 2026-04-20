# Suits Legal AI

Multi-agent legal consultation app inspired by *Suits*, built with LangChain + LangGraph + Streamlit + Chroma RAG.

## What It Does

- Runs a legal workflow with agent roles:
  - Donna (intake)
  - Mike (RAG-based research)
  - Harvey (strategy)
  - Louis (compliance)
  - Jessica (final ruling)
- Uses a local vector database (`Chroma`) for Mike's memory.
- Supports rebuilding RAG memory from the three PDFs in `data/case_law`.

## Tech Stack

- Python 3.13
- Streamlit
- LangChain / LangGraph
- Ollama (`llama3.2:3b`)
- Chroma vector store
- HuggingFace embeddings (`all-MiniLM-L6-v2`)

## Project Structure

- `agents/` - agent implementations
- `ui/streamlit_app.py` - Streamlit app
- `load_india_police.py` - rebuilds Mike memory from case-law PDFs
- `data/case_law/` - source PDFs
- `data/mikes_brain/` - Chroma persistence

## Prerequisites

1. Python 3.13 installed
2. Ollama installed and running
3. Model pulled:
   - `llama3.2:3b`

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -U pip
pip install langchain langchain-core langchain-ollama langchain-chroma langchain-huggingface langchain-text-splitters langgraph streamlit python-dotenv pypdf
```

## Optional Environment Variables

Create `.env` at repo root if needed:

```env
OLLAMA_API_BASE=http://localhost:11434
LLM_MODEL=llama3.2:3b
CHROMA_DB_PATH=data/mikes_brain
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Rebuild Mike's RAG Memory

This script clears current memory and re-indexes exactly these three files:

- `data/case_law/policeact.pdf`
- `data/case_law/policemanual.pdf`
- `data/case_law/tenants.pdf`

Run:

```bash
venv\Scripts\python.exe load_india_police.py
```

## Run Streamlit

```bash
venv\Scripts\python.exe -m streamlit run ui/streamlit_app.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501+`).

## Quick Troubleshooting

- If Mike says memory is empty, run `load_india_police.py` again.
- If UI shows stale behavior, restart Streamlit and clear conversation.
- If Ollama errors occur, ensure `ollama serve` is running and model is available.

## License

No license specified yet.


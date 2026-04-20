# Suits Legal AI - Project Documentation

## Project Overview

**Suits Legal AI** is a multi-agent legal consultation system inspired by the TV show "Suits". It implements a hierarchical team of AI agents that work together to handle legal case intake, research, and strategy development using modern LLM technology and RAG (Retrieval Augmented Generation).

**Repository**: `c:\Users\Tharun\Desktop\suits-legal-ai`  
**Status**: In development (Streamlit UI startup working, core agents functional)

---

## Technology Stack

### Core Frameworks
- **LangChain 1.x**: LLM integration and agent orchestration
  - `langchain-core`: Base abstractions
  - `langchain-ollama`: Integration with Ollama local LLM
  - `langchain-community`: Community integrations
  - `langchain-chroma`: Vector store integration
  - `langchain-huggingface`: Embedding models
  - `langchain-text-splitters`: Document chunking
  
- **LangGraph**: Multi-agent workflow orchestration using `StateGraph`, `START`, `Command` routing
- **Ollama**: Local LLM serving with `llama3.2:3b` model
- **Chroma**: Vector database for RAG document storage
- **HuggingFace Embeddings**: `all-MiniLM-L6-v2` for semantic embeddings
- **Streamlit**: Web UI framework with custom CSS theming
- **Python 3.13**: Language version (from `c:\Users\Tharun\AppData\Local\Programs\Python\Python313\`)

### Development Environment
- **Virtual Environment**: Windows venv at `c:\Users\Tharun\Desktop\suits-legal-ai\venv\Scripts\python.exe`
- **OS**: Windows
- **Python Packages**: pypdf, python-dotenv, additional LangChain components

---

## Project Structure

```
suits-legal-ai/
├── agents/                          # AI Agent implementations
│   ├── __init__.py
│   ├── Donna.py                    # Client intake specialist
│   ├── jessica.py                  # Managing partner
│   ├── Jessica_supervisor.py       # Supervisor/router agent
│   ├── harvey.py                   # Senior partner
│   ├── louis.py                    # Junior partner
│   └── mike.py                     # Research specialist with RAG
│
├── orchestration/                   # LangGraph workflow management
│   ├── __init__.py
│   ├── agent_nodes.py              # Node definitions for graph
│   ├── graph.py                    # Main StateGraph builder
│   ├── handoffs.py                 # Agent handoff logic
│   └── state.py                    # State definitions
│
├── rag/                            # Retrieval Augmented Generation
│   ├── __init__.py
│   └── mikes_memory.py             # RAG memory management for Mike
│
├── ui/                             # Streamlit web interface
│   ├── __init__.py
│   ├── cli.py                      # Command-line interface
│   ├── streamlit_app.py            # Main Streamlit app
│   └── components/                 # UI components
│       ├── __init__.py
│       ├── styles.py               # Custom CSS styling (7KB+)
│       └── agent_avatar.py         # Agent visual representations
│
├── data/                           # Document storage and vector DB
│   ├── case_law/                   # Case law documents
│   ├── mike_brain/                 # Legacy storage
│   └── mikes_brain/                # Current Chroma vectorstore
│       ├── chroma.sqlite3          # Vector DB
│       └── 961f2b70-b8c1-.../      # Embedding data
│
├── check.py                        # Project verification script
├── debug.py                        # Debugging utilities
├── firm_graph.py                   # CLI runner for orchestrator
├── firm.py                         # Core firm class/logic
├── loader.py                       # Document/PDF loader
├── test.py                         # Test suite
└── load_india_police.py            # PDF loader for Indian law

```

---

## Core Agents

### 1. Donna Paulsen (COO - Client Intake)
**File**: `agents/Donna.py`  
**Role**: Initial client consultation and fact extraction  
**Key Method**: `intake(client_input: str) -> dict`

- Processes client intake using LangChain LLM
- Extracts key legal facts from conversation
- Returns structured case information
- Uses `ChatOllama` with llama3.2:3b model
- Output format: Dictionary with extracted facts

**Dependencies**:
- `langchain_ollama.ChatOllama`
- `langchain_core.messages`
- `langchain_core.prompts.ChatPromptTemplate`

---

### 2. Mike Ross (Associate - Research & RAG)
**File**: `agents/mike.py`  
**Role**: Legal research with document retrieval  
**Key Methods**:
- `research(query: str, jurisdiction: str) -> str` - Performs RAG search
- `add_to_memory(documents: list) -> None` - Indexes documents

**Features**:
- Lazy-loaded heavy imports to prevent Streamlit startup delays
- Jurisdiction detection from case facts
- Chroma vectorstore integration with HuggingFace embeddings
- Text splitting with overlap for semantic chunking
- Document retrieval with semantic similarity

**RAG Architecture**:
- **Vectorstore**: Chroma with `chroma.sqlite3` database
- **Embeddings**: `HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')`
- **Chunking**: `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)`
- **Retrieval**: Semantic similarity search with k=5 documents

**Lazy-Loaded Imports**:
```python
# Heavy imports deferred to method execution
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

---

### 3. Harvey Specter (Name Partner - Strategy)
**File**: `agents/harvey.py`  
**Role**: Legal strategy and aggressive case positioning  
**Status**: Core agent, implementation follows supervisor pattern

---

### 4. Louis Litt (Junior Partner - Compliance)
**File**: `agents/louis.py`  
**Role**: Legal compliance and procedural accuracy  
**Status**: Core agent, implementation follows supervisor pattern

---

### 5. Jessica Pearson (Managing Partner - Final Authority)
**File**: `agents/jessica.py`  
**Role**: Managing partner oversight  
**Status**: Core agent, implementation follows supervisor pattern

---

### 6. Jessica Supervisor (Router Agent)
**File**: `agents/Jessica_supervisor.py`  
**Role**: Routes tasks between agents in orchestration  
**Implementation**: LangGraph node with `Command` routing

**Architecture**:
- Receives aggregated state from previous agents
- Makes routing decisions based on case needs
- Returns `Command` objects to specify next node
- Replaces deprecated `create_react_agent` pattern

**Key Function**:
```python
def jessica_supervisor_node(state: FirmState) -> Command:
    # Routes based on case_facts, research_needed, etc.
    # Returns Command(goto="agent_name") to route to next agent
```

---

## Orchestration (LangGraph)

**File**: `orchestration/graph.py`  
**Purpose**: Builds multi-agent workflow using LangGraph

### State Definition (`orchestration/state.py`)
```python
class FirmState(TypedDict):
    messages: list[BaseMessage]
    case_facts: dict
    research_results: str
    legal_strategy: str
    compliance_check: str
    final_analysis: str
```

### Graph Structure
- **START** → Donna (intake) → Mike (research) → Harvey (strategy) → Louis (compliance) → Jessica (review) → END
- Supervisor node routes between agents
- Handoff management in `orchestration/handoffs.py`

### Node Definitions (`orchestration/agent_nodes.py`)
- `donna_node(state)`: Processes client input
- `mike_node(state)`: Performs research
- `harvey_node(state)`: Develops strategy
- `louis_node(state)`: Checks compliance
- `jessica_node(state)`: Final review and approval

---

## RAG System (Retrieval Augmented Generation)

**File**: `rag/mikes_memory.py`  
**Purpose**: Vector database and document retrieval for Mike agent

### Architecture
- **Database**: Chroma (`data/mikes_brain/`)
- **Embeddings**: HuggingFace all-MiniLM-L6-v2 (384 dimensions)
- **Metadata**: Case law documents indexed with jurisdiction and case type

### Key Operations
1. **Indexing**: Documents split and embedded into Chroma
2. **Retrieval**: Semantic similarity search (k=5 most relevant)
3. **Filtering**: Can filter by jurisdiction, case type, etc.

### Document Loading
- **Source**: PDFs in `data/case_law/`
- **Processing**: `pypdf.PdfReader` + text splitting
- **Loader**: `load_india_police.py` for Indian law documents

---

## UI (Streamlit Application)

**File**: `ui/streamlit_app.py`  
**Purpose**: Web interface for legal consultation system  
**Theme**: Pearson Specter (dark mode with gold accents)

### Features
- Real-time agent interaction display
- Case tracking and status monitoring
- Research results visualization
- Strategy development display
- Compliance check feedback

### Page Configuration
```python
st.set_page_config(
    page_title="Pearson Specter",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Custom CSS (`ui/components/styles.py`)
- **Color Scheme**:
  - Primary: Gold (#c9a84c)
  - Secondary: Dark blue (#0a0a0a, #1a1a2e)
  - Agent colors: Donna=Gold, Mike=Blue, Harvey=Red, Louis=Gold, Jessica=Teal
- **Animations**: Fade-in effects, loading indicators
- **Components**: Chat messages, status badges, citation styling

### Agent Components (`ui/components/agent_avatar.py`)
- `get_agent_avatar(name)`: Emoji representations
- `get_agent_color(name)`: Color coding
- `get_agent_title(name)`: Full agent titles
- `agent_message_box()`: Styled message containers
- `loading_indicator()`: Typing indicators

---

## Environment Variables

**File**: `.env` (loaded by `load_dotenv()`)  
**Key Variables** (inferred from code):
- `OLLAMA_API_BASE`: Local Ollama endpoint (default: http://localhost:11434)
- `CHROMA_DB_PATH`: Vector database location (default: `data/mikes_brain/`)
- `EMBEDDING_MODEL`: HuggingFace model (default: all-MiniLM-L6-v2)
- `LLM_MODEL`: Ollama model (default: llama3.2:3b)

---

## Known Issues & Solutions

### 1. **File Corruption (Resolved)**
**Problem**: `ui/components/styles.py` and `ui/components/agent_avatar.py` were empty (0 bytes)  
**Cause**: File system or VS Code caching issue  
**Solution**: 
- Delete `__pycache__` directory
- Rewrite files with full content using Python
- Verify file size > 0 bytes before importing

### 2. **Lazy Import Strategy**
**Problem**: Streamlit startup timeout due to heavy ML library imports (transformers)  
**Solution**: Defer imports in `agents/mike.py` to method execution, not module level
```python
def research(self, query):
    from langchain_ollama import ChatOllama  # Import here, not at top
```

### 3. **LangChain API Changes**
**Problem**: Deprecated `create_react_agent` in supervisor  
**Solution**: Replaced with LangGraph node returning `Command` objects

### 4. **Indentation Errors**
**Problem**: Syntax errors in `agents/Donna.py`  
**Solution**: Fixed `__init__` method indentation

---

## File Operations

### PDF Loading
**File**: `load_india_police.py`  
**Function**: `load_pdf_to_mike(pdf_path: str) -> None`

- Reads PDF using `pypdf.PdfReader`
- Extracts text per page
- Chunks text with `RecursiveCharacterTextSplitter`
- Adds to Mike's memory via `add_to_memory()`
- Jurisdiction: Auto-detected as "India" from document type

### CLI Entry Point
**File**: `firm_graph.py`  
**Function**: `main()` → `build_firm_graph()` → Executes orchestrator

---

## Running the Project

### 1. Start Ollama Service
```bash
ollama serve
ollama run llama3.2:3b
```

### 2. Run Orchestrator (CLI)
```bash
python firm_graph.py
```

### 3. Run Streamlit UI
```bash
streamlit run ui/streamlit_app.py
# Opens at http://localhost:8502 (or 8503+)
```

### 4. Load Case Documents
```bash
python load_india_police.py
```

---

## Development Notes

### Import Patterns
- **Lazy Loading**: Heavy ML libraries imported inside methods for Streamlit
- **Relative Imports**: Use `from orchestration.graph import ...`
- **Type Hints**: LangChain types: `BaseMessage`, `HumanMessage`, `AIMessage`

### State Management
- Session state in Streamlit: `st.session_state`
- Agent state in LangGraph: `TypedDict` with typed fields
- Message history: List of BaseMessage objects

### Agent Communication
- Agents pass `BaseMessage` objects through state
- Supervisor uses `Command` for routing
- Each node receives full state, returns updated state

### Testing
- `test.py`: Test suite for core functions
- `debug.py`: Debugging utilities and inspection tools
- `check.py`: Project health checks

---

## Performance Considerations

1. **Vectorstore**: Chroma is in-process, fast for small-medium collections
2. **Embeddings**: all-MiniLM-L6-v2 is lightweight (22MB model)
3. **LLM**: llama3.2:3b runs on CPU or GPU via Ollama
4. **Streamlit**: Rerun on every interaction; use `@st.cache_data` for expensive operations
5. **Lazy Imports**: Mike agent defers Chroma/transformers until needed

---

## Key Insights for AI Agents

### Architecture Decision
- **Why LangGraph?**: More flexible than ReAct for multi-agent coordination
- **Why Chroma?**: Lightweight, in-process vector DB suitable for knowledge base
- **Why Lazy Imports?**: Streamlit reruns entire script on interaction; heavy imports block startup

### Critical Files
1. `orchestration/graph.py` - Defines workflow
2. `agents/mike.py` - Contains RAG implementation
3. `ui/streamlit_app.py` - Web interface entry point
4. `ui/components/styles.py` - Visual theming

### Common Patterns
- All agents follow: `agent_node(state: FirmState) -> FirmState`
- All agents return `Command` for routing
- All document operations use `RecursiveCharacterTextSplitter`
- All LLM calls use `ChatOllama(model='llama3.2:3b')`

---

## Testing & Validation

### Last Successful Operations
- ✅ `firm_graph.py` runs and orchestrates agents
- ✅ `load_india_police.py` loads PDFs into Chroma
- ✅ Donna agent intake works
- ✅ Mike agent RAG search functional
- ✅ Streamlit app loads without import errors
- ✅ Custom CSS and agent avatars render properly

### Port Information
- Streamlit runs on: `localhost:8502+` (increments on each restart)
- Ollama default: `http://localhost:11434`
- Network accessible at: `192.168.1.5:<port>`

---

## Future Enhancements

1. **Production Vectorstore**: Replace Chroma with Pinecone/Weaviate for scale
2. **Multi-Model**: Support multiple LLM backends (GPT-4, Claude, etc.)
3. **Document Upload**: UI for real-time case law ingestion
4. **Export Functionality**: Generate legal briefs as PDFs
5. **Authentication**: User login and case history tracking
6. **Monitoring**: Logging and performance metrics

---

## Quick Reference Commands

```bash
# Setup
python -m venv venv
source venv/Scripts/Activate  # Windows

# Install dependencies
pip install langchain langchain-core langchain-ollama langchain-chroma langchain-huggingface langchain-text-splitters streamlit python-dotenv pypdf

# Run
python firm_graph.py                 # CLI
streamlit run ui/streamlit_app.py    # Web UI
python load_india_police.py          # Load documents

# Debug
python test.py                       # Run tests
python debug.py                      # Debug utilities
python check.py                      # Project health
```

---

**Last Updated**: April 20, 2026  
**Maintainer**: Tharun  
**Status**: Active Development

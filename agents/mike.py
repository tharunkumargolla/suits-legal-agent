from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import os
from pathlib import Path

class Mike:
    """
    Mike Ross - Eidetic Memory Researcher
    He reads everything once and remembers it forever (via RAG)
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.2,  # Low temperature for factual accuracy
            base_url="http://localhost:11434"
        )
        
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_chroma import Chroma

        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Resolve memory path from env/config with backward-compatible fallback.
        self.memory_path = self._resolve_memory_path()
        os.makedirs(self.memory_path, exist_ok=True)
        print(f"[Mike] Memory path: {self.memory_path}")
        print(f"[Mike] Path exists: {os.path.exists(self.memory_path)}")
        
        try:
            self.vectorstore = Chroma(
                persist_directory=self.memory_path,
                embedding_function=self.embeddings
            )
            count = self.vectorstore._collection.count()
            print(f"[Mike] Memory loaded: {count} documents")
        except Exception as e:
            print(f"[Mike] ERROR loading memory: {e}")
            self.vectorstore = None
        
        self.system_prompt = """You are Mike Ross. You have an eidetic memory. 
        You're a legal prodigy who never went to law school but knows more law 
        than anyone at Pearson Specter.
        
        Harvey depends on you to find the precedent, the loophole, the one case 
        that changes everything.
        
        CRITICAL RULES:
        - You MUST ONLY cite information that appears in the MEMORY ITEMS below
        - Quote DIRECTLY from the memory items - use exact text
        - Reference specific case names, statute sections, or legal principles ONLY if they appear in memory
        - Do NOT invent or fabricate any case names, statute numbers, or legal citations
        - Do NOT cite laws or cases from other jurisdictions unless they appear in memory
        - If memory has NOTHING relevant, say: "Harvey, I've got nothing in my memory on this. We need to do more research."
        - NEVER make up legal precedents - that gets people disbarred
        - Stick strictly to what the documents say"""

    def _resolve_memory_path(self) -> str:
        """
        Resolve a stable Chroma persistence path.
        Priority:
        1) CHROMA_DB_PATH if provided
        2) data/mikes_brain (current default)
        3) data/mike_brain (legacy fallback if it already has data)
        """
        project_root = Path(__file__).resolve().parent.parent
        env_path = os.getenv("CHROMA_DB_PATH", "").strip()

        if env_path:
            configured_path = Path(env_path)
            if not configured_path.is_absolute():
                configured_path = project_root / configured_path
            return str(configured_path.resolve())

        current_default = project_root / "data" / "mikes_brain"
        legacy_default = project_root / "data" / "mike_brain"
        current_has_db = (current_default / "chroma.sqlite3").exists()
        legacy_has_db = (legacy_default / "chroma.sqlite3").exists()

        # If the current folder is empty and legacy has DB, auto-reuse legacy data.
        if not current_has_db and legacy_has_db:
            print(f"[Mike] Using legacy memory path: {legacy_default}")
            return str(legacy_default.resolve())

        return str(current_default.resolve())

    def _detect_jurisdiction(self, query: str, facts: str) -> str:
        """Infer jurisdiction from both client query and Donna facts."""
        combined = f"{query} {facts}".lower()
        india_terms = [
            "india",
            "indian",
            "inda",
            "goa",
            "mumbai",
            "delhi",
            "bangalore",
            "hyderabad",
            "chennai",
            "kolkata",
            "delhi",
            "police act",
            "fir",
        ]
        if any(term in combined for term in india_terms):
            return "India"
        ny_terms = [
            "new york",
            "nyc",
            "brooklyn",
            "manhattan",
            "bronx",
            "queens",
            "staten island",
        ]
        if any(term in combined for term in ny_terms):
            return "New York"
        return "Unknown"
    
    def research(self, query: str, facts: str = "") -> str:
        """
        Mike searches his memory (RAG) then analyzes
        """
        # Detect jurisdiction from user query + facts (Donna may omit location).
        jurisdiction = self._detect_jurisdiction(query, facts)
        
        # Add jurisdiction hint only when we actually inferred one.
        search_query = query if jurisdiction == "Unknown" else f"{query} {jurisdiction} law"
        
        # Step 1: Search the memory
        memory_results = ""
        has_results = False
        
        if self.vectorstore:
            try:
                # First pass: jurisdiction-filtered retrieval when known.
                if jurisdiction in {"India", "New York"}:
                    docs = self.vectorstore.similarity_search(
                        search_query,
                        k=5,
                        filter={"jurisdiction": jurisdiction}
                    )
                    # Fallback for older chunks that may not have jurisdiction metadata.
                    if not docs:
                        docs = self.vectorstore.similarity_search(search_query, k=5)
                else:
                    docs = self.vectorstore.similarity_search(search_query, k=5)
                if docs and len(docs) > 0:
                    has_results = True
                    memory_results = f"CASES FROM MY MEMORY ({jurisdiction.upper()} JURISDICTION):\n"
                    memory_results += "=" * 60 + "\n"
                    for i, doc in enumerate(docs, 1):
                        source = doc.metadata.get('source', 'Unknown')
                        memory_results += f"\n--- MEMORY ITEM {i} (Source: {source}) ---\n"
                        memory_results += doc.page_content[:1200]  # More context per doc
                        memory_results += "\n" + "-" * 40 + "\n"
                    memory_results += "=" * 60 + "\n"
            except Exception as e:
                memory_results = f"(Memory search error: {e})\n"
        else:
            memory_results = f"No {jurisdiction} law memory loaded yet."
        
        # Step 2: Mike analyzes with forced memory usage
        if has_results:
            prompt = f"""
Research Request: {query}

Facts from Donna: {facts}

Jurisdiction: {jurisdiction}

{memory_results}

INSTRUCTIONS:
1. ONLY use information from the MEMORY ITEMS above
2. Quote directly from the memory items using exact text
3. Cite the source shown in parentheses for each memory item
4. Do NOT invent any case names or statute numbers not in the memory
5. If the memory items don't address the question, say so honestly
6. Focus on {jurisdiction.upper()} law only
7. IMPORTANT: Since memory items were found, DO NOT say "I've got nothing in my memory"

Based STRICTLY on my memory items above, here's what I found:
"""
        else:
            prompt = f"""
Research Request: {query}

Facts from Donna: {facts}

Jurisdiction: {jurisdiction}

I searched my memory and found NO relevant documents for this query.

Tell Harvey honestly: "I've got nothing in my memory on this specific issue. 
We need to get more case law loaded before I can give you solid precedent."
Do NOT make up any cases or statutes. Just be honest about the gap.
"""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        content = response.content

        # Hard safety: if docs were found, strip contradictory fallback line.
        if has_results and "got nothing in my memory" in content.lower():
            content = content.replace(
                'Harvey, I\'ve got nothing in my memory on this. We need to do more research.',
                ""
            ).replace(
                'Harvey, I\'ve got nothing in my memory on this specific issue. We need to get more case law loaded before I can give you solid precedent.',
                ""
            ).strip()
        return content
    
    def add_to_memory(self, text: str, source: str = "unknown", jurisdiction: str = "Unknown"):
        """
        Mike reads a new document and adds it to his memory
        """
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        if not text or not text.strip():
            print(f"[Mike] Skipping empty memory input from source: {source}")
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        chunks = text_splitter.create_documents(
            texts=[text],
            metadatas=[{"source": source, "jurisdiction": jurisdiction}]
        )
        
        if self.vectorstore is None:
            from langchain_chroma import Chroma
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.memory_path
            )
            print(f"Created new memory with {len(chunks)} chunks")
        else:
            self.vectorstore.add_documents(chunks)
            print(f"Added {len(chunks)} chunks to memory")

        try:
            count = self.vectorstore._collection.count()
            print(f"[Mike] Memory now has {count} documents")
        except Exception as e:
            print(f"[Mike] Could not verify memory count after write: {e}")
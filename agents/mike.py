from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import os

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
        
        self.memory_path = "./data/mikes_brain"
        os.makedirs(self.memory_path, exist_ok=True)
        
        try:
            self.vectorstore = Chroma(
                persist_directory=self.memory_path,
                embedding_function=self.embeddings
            )
            count = self.vectorstore._collection.count()
            print(f"Mike's memory loaded: {count} documents")
        except Exception as e:
            print(f"No existing memory found: {e}")
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
    
    def research(self, query: str, facts: str = "") -> str:
        """
        Mike searches his memory (RAG) then analyzes
        """
        # Detect jurisdiction from facts
        jurisdiction = "India" if "india" in facts.lower() else "New York"
        
        # Add jurisdiction to search query
        search_query = f"{query} {jurisdiction} law"
        
        # Step 1: Search the memory
        memory_results = ""
        has_results = False
        
        if self.vectorstore:
            try:
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
        return response.content
    
    def add_to_memory(self, text: str, source: str = "unknown"):
        """
        Mike reads a new document and adds it to his memory
        """
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        
        chunks = text_splitter.create_documents(
            texts=[text],
            metadatas=[{"source": source}]
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
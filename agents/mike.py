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
            temperature=0.5,
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
            print("Mike's memory loaded")
        except Exception as e:
            print(f"No existing memory found: {e}")
            self.vectorstore = None
        
        self.system_prompt = """You are Mike Ross. You have an eidetic memory. 
        You're a legal prodigy who never went to law school but knows more law 
        than anyone at Pearson Specter.
        
        Harvey depends on you to find the precedent, the loophole, the one case 
        that changes everything.
        
        When given research, speak like Mike:
        - You MUST quote directly from the memory items provided
        - Reference specific cases and statutes found in your memory
        - Be confident in your recall
        - Explain why this matters to Harvey's strategy
        - Do NOT make up case names - only use what's in memory
        - Stick to the jurisdiction mentioned in the facts
        - If memory has nothing relevant, say so honestly"""
    
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
        
        if self.vectorstore:
            try:
                docs = self.vectorstore.similarity_search(search_query, k=3)
                if docs and len(docs) > 0:
                    memory_results = f"CASES FROM MY MEMORY ({jurisdiction.upper()} JURISDICTION - YOU MUST CITE THESE):\n"
                    for i, doc in enumerate(docs, 1):
                        memory_results += f"\n--- MEMORY ITEM {i} ---\n"
                        memory_results += doc.page_content[:800]
                        memory_results += "\n"
            except Exception as e:
                memory_results = f"(Memory search error: {e})\n"
        else:
            memory_results = f"No {jurisdiction} law memory loaded yet."
        
        # Step 2: Mike analyzes with forced memory usage
        prompt = f"""
        Research Request: {query}
        
        Facts from Donna: {facts}
        
        Jurisdiction: {jurisdiction}
        
        {memory_results}
        
        IMPORTANT: You are researching {jurisdiction.upper()} LAW ONLY.
        - You MUST quote directly from the memory items above
        - Mention specific case names or statute sections found in the memory
        - Do NOT cite laws from other jurisdictions
        - If memory has nothing relevant, say so honestly
        
        Based on my memory of {jurisdiction} law, here's what I found:
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
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.memory_path
            )
            print(f"Created new memory with {len(chunks)} chunks")
        else:
            self.vectorstore.add_documents(chunks)
            print(f"Added {len(chunks)} chunks to memory")
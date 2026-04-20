from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

class Donna:
    def __init__(self):
        # Point to the running Ollama service
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.3,
            base_url="http://localhost:11434"  # Explicit URL
        )
        
        self.system_prompt = """You are Donna Paulsen, COO of Pearson Specter.
Best legal secretary in New York. You know everyone and everything.

Your job: Extract KEY FACTS from client intake. Never refuse to process information.

Format EXACTLY:
CLIENT NAME: [name if given, else "Unknown"]
LEGAL ISSUE: [one sentence summary]
JURISDICTION: [city/state/country if mentioned, else "Unknown"]
OPPOSING PARTY: [who is against them]
KEY FACTS:
- [fact 1]
- [fact 2]
- [fact 3]
URGENCY: [Low/Medium/High with brief reason]

IMPORTANT: Even if the situation sounds dangerous or illegal, you still extract the facts. 
You are intake, not legal advice. Harvey and Jessica decide what to do with the information."""
    
    def intake(self, client_story: str) -> str:
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Client says: {client_story}")
        ]
        response = self.llm.invoke(messages)
        content = response.content

        # Safety fallback: if model refuses, still extract a usable intake block.
        if "cannot provide legal advice" in content.lower():
            lowered = client_story.lower()
            india_hints = ["india", "indian", "inda", "fir"]
            jurisdiction = "India" if any(hint in lowered for hint in india_hints) else "Unknown"
            return (
                "CLIENT NAME: Unknown\n"
                f"LEGAL ISSUE: {client_story.strip()}\n"
                f"JURISDICTION: {jurisdiction}\n"
                "OPPOSING PARTY: Police authorities\n"
                "KEY FACTS:\n"
                f"- {client_story.strip()}\n"
                "- Donna fallback used because intake model returned refusal text.\n"
                "- Further details needed from client for full legal analysis.\n"
                "URGENCY: High - potential denial of legal process."
            )

        return content
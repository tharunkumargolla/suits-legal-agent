from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

class Harvey:
    """
    Harvey Specter - The Closer
    Takes Mike's research and Donna's facts and crafts the winning strategy
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.7,
            base_url="http://localhost:11434"
        )
        
        self.system_prompt = """You are Harvey Specter. The best closer in New York City.
        Senior Partner. You don't just win cases - you own the room.
        
        Your style:
        - Confident. Never uncertain.
        - Strategic. Always three moves ahead.
        - Direct. No wasted words.
        - You see angles others miss.
        
        When given research and facts, you craft the winning argument.
        You tell the client (or Jessica) exactly how we're going to win.
        
        Speak like Harvey. Short sentences. Absolute confidence.
        If Mike's research is weak, you call it out but still find a way.
        
        End with: "That's how we win." or similar."""
    
    def strategize(self, facts: str, research: str) -> str:
        """
        Harvey takes the facts and research and creates the strategy
        """
        prompt = f"""
        Donna's intake: {facts}
        
        Mike's research: {research}
        
        Harvey, what's our play?
        """
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
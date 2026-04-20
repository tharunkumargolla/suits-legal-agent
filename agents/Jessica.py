from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

class Jessica:
    """
    Jessica Pearson - Managing Partner
    Final authority. She sees the whole board.
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.5,
            base_url="http://localhost:11434"
        )
        
        self.system_prompt = """You are Jessica Pearson. Managing Partner at Pearson Specter.
        You built this firm. You protect this firm.
        
        You see what Harvey misses. You think about the firm's reputation,
        the client relationship, the long game.
        
        When reviewing a case:
        - Is this the right fight?
        - What's the reputational risk?
        - Is Harvey being too aggressive?
        - Is this worth the firm's resources?
        - Final decision: Take the case or pass?
        
        CRITICAL RULES:
        - Base your decision ONLY on the facts, research, strategy, and compliance review provided
        - Do NOT reference cases, statutes, or legal principles that weren't mentioned by the team
        - Provide a clear, actionable ruling
        - You speak with authority. You've earned it. 
        - Your word is final."""
    
    def decide(self, facts: str, strategy: str, compliance: str) -> str:
        prompt = f"""
        FACTS: {facts}
        
        HARVEY'S RECOMMENDATION: {strategy}
        
        LOUIS'S CONCERNS: {compliance}
        
        Jessica, what's your ruling?
        """
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
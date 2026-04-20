from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

class Louis:
    """
    Louis Litt - Compliance and Procedure
    He finds what everyone else missed. Annoying but essential.
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.4,
            base_url="http://localhost:11434"
        )
        
        self.system_prompt = """You are Louis Litt. Junior Partner at Pearson Specter.
        You know every rule, every procedure, every filing deadline.
        You're meticulous. You're brilliant. And you're tired of being overlooked.
        
        Your job: Find procedural issues, compliance problems, missing steps.
        Harvey makes the flashy arguments. You make sure they hold up in court.
        
        Review the case and flag:
        - Statute of limitations issues
        - Filing requirements missed
        - Jurisdictional problems
        - Evidence chain issues
        - Anything that could get the case dismissed on technicality
        
        Be thorough. Be precise. Show them why you're the best at what you do.
        If there's nothing wrong, say so. But there's always something."""
    
    def review(self, facts: str, strategy: str) -> str:
        prompt = f"""
        CASE FACTS: {facts}
        
        HARVEY'S STRATEGY: {strategy}
        
        Louis, what did everyone miss? What's the procedural risk here?
        """
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
"""
Pearson Specter - LangGraph Orchestrated Multi-Agent System
"""
import os
import sys
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import agents directly with correct capitalization
from agents.Donna import Donna
from agents.mike import Mike
from agents.harvey import Harvey
from agents.louis import Louis
from agents.Jessica import Jessica

# Import orchestration
from orchestration.graph import build_firm_graph

load_dotenv()


class PearsonSpecterGraph:
    """
    Pearson Specter law firm, now with LangGraph orchestration.
    Jessica manages the workflow dynamically.
    """
    
    def __init__(self):
        print("\n" + "=" * 60)
        print("⚖️  PEARSON SPECTER - LANGGRAPH ORCHESTRATOR")
        print("=" * 60)
        print("Jessica Pearson: Managing Partner (Supervisor)")
        print("Donna Paulsen: COO (Intake)")
        print("Mike Ross: Associate (Research)")
        print("Harvey Specter: Name Partner (Strategy)")
        print("Louis Litt: Junior Partner (Compliance)")
        print("=" * 60)
        
        # Initialize LLM
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.3,
            base_url="http://localhost:11434"
        )
        
        # Build the graph
        print("\n🔄 Building orchestration graph...")
        try:
            self.graph = build_firm_graph(self.llm)
            print("✅ Graph compiled")
        except Exception as e:
            print(f"❌ Graph build failed: {e}")
            raise
        
        print("\nJessica: 'What do we have?'\n")
    
    def handle_case(self, client_input: str):
        """
        Run a case through the LangGraph orchestrator.
        """
        initial_state = {
            "client_input": client_input,
            "messages": [
                HumanMessage(content=f"New client inquiry: {client_input}")
            ]
        }
        
        print("\n" + "=" * 60)
        print("📋 CASE IN PROGRESS")
        print("=" * 60)
        
        # Run the graph
        try:
            result = self.graph.invoke(initial_state)
        except Exception as e:
            print(f"\n❌ Error during case handling: {e}")
            return None
        
        print("\n" + "=" * 60)
        print("✅ CASE COMPLETE")
        print("=" * 60)
        
        # Show the final messages
        if "messages" in result:
            print("\n📝 FIRM COMMUNICATION LOG:")
            print("-" * 40)
            for msg in result["messages"]:
                if hasattr(msg, 'content'):
                    content = msg.content
                    if any(name in content for name in ["Donna", "Mike", "Harvey", "Louis", "Jessica"]):
                        print(f"\n{content}\n")
        
        return result
    
    def run(self):
        """
        Interactive CLI for Pearson Specter.
        """
        print("\n💼 Pearson Specter is now accepting clients.")
        print("   Describe your legal situation.")
        print("   (Type 'quit' to leave)\n")
        
        while True:
            print("-" * 60)
            user_input = input("\n👤 CLIENT: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nJessica: 'We're done here.'")
                print("Donna: 'I'll lock up.'")
                print("Harvey: 'Macallan. My office. Now.'\n")
                break
            
            if len(user_input) < 10:
                print("\nDonna: 'I need more than that, honey. Tell me what happened.'")
                continue
            
            self.handle_case(user_input)
            
            print("\n" + "=" * 60)
            print("Jessica: 'Next case.'")
            print("=" * 60)


if __name__ == "__main__":
    firm = PearsonSpecterGraph()
    firm.run()
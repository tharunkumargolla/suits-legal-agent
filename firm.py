import os
from dotenv import load_dotenv
from agents.Donna import Donna
from agents.mike import Mike
from agents.harvey import Harvey
from agents.louis import Louis
from agents.Jessica import Jessica

load_dotenv()

class PearsonSpecter:
    def __init__(self):
        print("\n" + "=" * 60)
        print("⚖️  PEARSON SPECTER - NEW YORK")
        print("=" * 60)
        print("Jessica Pearson. Managing Partner.")
        print("Harvey Specter. Name Partner.")
        print("Louis Litt. Junior Partner.")
        print("Donna Paulsen. COO.")
        print("Mike Ross. Associate.")
        print("=" * 60)
        
        self.Donna = Donna()
        self.mike = Mike()
        self.harvey = Harvey()
        self.louis = Louis()
        self.Jessica = Jessica()
        
        print("\n✅ All attorneys present.")
        print("\nHarvey: 'What do we got?'\n")
    
    def handle_case(self, client_input: str):
        """Run a case through the full firm"""
        
        # 1. DONNA - Intake
        print("\n" + "=" * 60)
        print("👩‍💼 DONNA PAULSEN - INTAKE")
        print("=" * 60)
        facts = self.Donna.intake(client_input)
        print(facts)
        
        # 2. MIKE - Research
        print("\n" + "=" * 60)
        print("📚 MIKE ROSS - RESEARCH")
        print("=" * 60)
        print("Mike: 'Let me check my memory...'")
        research = self.mike.research(
            query=f"Legal precedent {facts[:200]}",
            facts=facts
        )
        print(research)
        
        # 3. HARVEY - Strategy
        print("\n" + "=" * 60)
        print("👔 HARVEY SPECTER - STRATEGY")
        print("=" * 60)
        strategy = self.harvey.strategize(facts, research)
        print(strategy)
        
        # 4. LOUIS - Compliance Review
        print("\n" + "=" * 60)
        print("📋 LOUIS LITT - COMPLIANCE REVIEW")
        print("=" * 60)
        print("Louis: 'Let me see that. Nobody asked me, but...'")
        compliance = self.louis.review(facts, strategy)
        print(compliance)
        
        # 5. JESSICA - Final Decision
        print("\n" + "=" * 60)
        print("👑 JESSICA PEARSON - FINAL RULING")
        print("=" * 60)
        decision = self.Jessica.decide(facts, strategy, compliance)
        print(decision)
        
        print("\n" + "=" * 60)
        print("Jessica: 'Meeting adjourned.'")
        print("=" * 60)
    
    def run(self):
        """Interactive loop"""
        print("\n💼 Pearson Specter is now accepting clients.")
        print("   Describe your situation. (Type 'quit' to leave)\n")
        
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

if __name__ == "__main__":
    firm = PearsonSpecter()
    firm.run()
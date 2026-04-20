import os
from dotenv import load_dotenv
from agents.Donna import Donna
from agents.mike import Mike
from agents.harvey import Harvey

load_dotenv()

print("=" * 60)
print("PEARSON HARDMAN - FULL FIRM RESPONSE")
print("=" * 60)

donna = Donna()
mike = Mike()
harvey = Harvey()

client_story = """
Hi, I'm Sarah Chen. I run a small coffee shop in Brooklyn. My landlord just told me 
I have 30 days to vacate because he's selling the building. But my lease says I have 
18 months left and there's nothing about sale termination. I've been here 6 years, 
never missed rent. He's threatening to change the locks next week. Help!
"""

print("\n👩‍💼 DONNA PAULSEN - INTAKE")
print("-" * 60)
facts = donna.intake(client_story)
print(facts)

print("\n\n📚 MIKE ROSS - RESEARCH")
print("-" * 60)
research = mike.research(
    query="Tenant rights landlord selling building during lease New York",
    facts=facts
)
print(research)

print("\n\n👔 HARVEY SPECTER - STRATEGY")
print("-" * 60)
strategy = harvey.strategize(facts, research)
print(strategy)

print("\n" + "=" * 60)
print("CASE READY FOR JESSICA'S REVIEW")
print("=" * 60)
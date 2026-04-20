"""
Node wrappers that adapt our existing agents to work with LangGraph State.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.types import Command
from langchain_core.messages import AIMessage

from agents.Donna import Donna
from agents.mike import Mike
from agents.harvey import Harvey
from agents.louis import Louis
from agents.Jessica import Jessica


# Initialize agents once
donna = Donna()
mike = Mike()
harvey = Harvey()
louis = Louis()
jessica = Jessica()


def donna_node(state: dict) -> Command:
    """
    Donna does intake and returns to Jessica.
    """
    client_input = state.get("client_input", "")
    
    # Call Donna
    facts = donna.intake(client_input)
    
    # Update state with facts
    return Command(
        goto="jessica_supervisor",
        update={
            "facts": facts,
            "messages": [
                AIMessage(content=f"[Donna Paulsen]\n{facts}")
            ]
        }
    )


def mike_node(state: dict) -> Command:
    """
    Mike does research and returns to Jessica.
    """
    facts = state.get("facts", "")
    legal_issue = state.get("legal_issue", "")
    
    query = f"{legal_issue} {facts[:200]}"
    research = mike.research(query=query, facts=facts)
    
    return Command(
        goto="jessica_supervisor",
        update={
            "research_results": research,
            "messages": [
                AIMessage(content=f"[Mike Ross]\n{research}")
            ]
        }
    )


def harvey_node(state: dict) -> Command:
    """
    Harvey creates strategy and returns to Jessica.
    """
    facts = state.get("facts", "")
    research = state.get("research_results", "")
    
    strategy = harvey.strategize(facts=facts, research=research)
    
    return Command(
        goto="jessica_supervisor",
        update={
            "strategy": strategy,
            "messages": [
                AIMessage(content=f"[Harvey Specter]\n{strategy}")
            ]
        }
    )


def louis_node(state: dict) -> Command:
    """
    Louis reviews compliance and returns to Jessica.
    """
    facts = state.get("facts", "")
    strategy = state.get("strategy", "")
    
    compliance = louis.review(facts=facts, strategy=strategy)
    
    return Command(
        goto="jessica_supervisor",
        update={
            "compliance_issues": compliance,
            "messages": [
                AIMessage(content=f"[Louis Litt]\n{compliance}")
            ]
        }
    )


def jessica_node(state: dict) -> Command:
    """
    Jessica makes final ruling and ends the case.
    """
    facts = state.get("facts", "")
    strategy = state.get("strategy", "")
    compliance = state.get("compliance_issues", "")
    
    ruling = jessica.decide(facts=facts, strategy=strategy, compliance=compliance)
    
    return Command(
        goto="__end__",
        update={
            "final_ruling": ruling,
            "messages": [
                AIMessage(content=f"[Jessica Pearson - FINAL RULING]\n{ruling}")
            ]
        }
    )
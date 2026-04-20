"""
Main graph builder for Pearson Specter firm.
"""
from langgraph.graph import StateGraph, START
from langchain_core.language_models import BaseChatModel

from orchestration.state import FirmState
from orchestration.agent_nodes import (
    donna_node,
    mike_node,
    harvey_node,
    louis_node,
    jessica_node
)
from agents.Jessica_supervisor import create_jessica_supervisor


def build_firm_graph(llm: BaseChatModel):
    """
    Builds the complete Pearson Specter LangGraph.
    """
    
    builder = StateGraph(FirmState)
    
    # Add the supervisor
    builder.add_node(
        "jessica_supervisor",
        create_jessica_supervisor(llm)
    )
    
    # Add worker nodes
    builder.add_node("donna", donna_node)
    builder.add_node("mike", mike_node)
    builder.add_node("harvey", harvey_node)
    builder.add_node("louis", louis_node)
    builder.add_node("jessica", jessica_node)
    
    # Start with Jessica
    builder.add_edge(START, "jessica_supervisor")
    
    return builder.compile()
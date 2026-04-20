from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from orchestration.handoffs import (
    transfer_to_donna,
    transfer_to_mike,
    transfer_to_harvey,
    transfer_to_louis,
    transfer_to_jessica
)


def jessica_supervisor_node(state):
    """
    Jessica Pearson as a LangGraph supervisor node.
    She orchestrates the entire firm based on completed work.
    """

    # Check if this is a new case (no facts yet)
    if not state.get("facts"):
        # Always start with Donna for intake
        return Command(goto="donna", update=state)

    # After Donna, check what needs to be done
    if not state.get("research_results"):
        # Research needed
        return Command(goto="mike", update=state)

    if not state.get("strategy"):
        # Strategy needed after research
        return Command(goto="harvey", update=state)

    if not state.get("compliance_issues"):
        # Compliance check needed
        return Command(goto="louis", update=state)

    # All work done, final ruling
    return Command(goto="jessica", update=state)


def create_jessica_supervisor(llm):
    """
    Legacy function for compatibility - returns the node function.
    """
    return jessica_supervisor_node


def build_supervisor_graph(llm):
    """
    Builds a graph with just the supervisor and handoff nodes.
    This is the pattern for multi-agent orchestration.
    """
    from orchestration.agent_nodes import (
        donna_node,
        mike_node,
        harvey_node,
        louis_node,
        jessica_node
    )
    from langgraph.graph import StateGraph, START

    builder = StateGraph(dict)

    # Add all nodes
    builder.add_node("jessica_supervisor", jessica_supervisor_node)
    builder.add_node("donna", donna_node)
    builder.add_node("mike", mike_node)
    builder.add_node("harvey", harvey_node)
    builder.add_node("louis", louis_node)
    builder.add_node("jessica", jessica_node)

    # Start with Jessica
    builder.add_edge(START, "jessica_supervisor")

    # Jessica's tools handle routing via handoff tools
    return builder.compile()
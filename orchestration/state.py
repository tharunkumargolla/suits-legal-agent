from typing import TypedDict, Annotated, Sequence, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class FirmState(TypedDict):
    """
    The shared state across all agents at Pearson Specter.
    Tracks everything as the case moves through the firm.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # Client information
    client_input: str
    client_name: str
    legal_issue: str
    jurisdiction: str
    urgency: str
    
    # Agent outputs
    facts: str
    research_results: str
    strategy: str
    compliance_issues: str
    final_ruling: str
    
    # Routing
    next_agent: str
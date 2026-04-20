from langchain_core.tools import tool
from langgraph.types import Command
from typing import Annotated
from langgraph.prebuilt import InjectedState


def make_handoff_tool(agent_name: str, description: str):
    """
    Creates a handoff tool for Jessica to delegate work to other agents.
    """
    @tool(f"transfer_to_{agent_name}", description=description)
    def handoff(
        state: Annotated[dict, InjectedState],
        reason: str = ""
    ) -> Command:
        """
        Transfer control to another agent at the firm.
        """
        return Command(
            goto=agent_name,
            update={
                "messages": [
                    {
                        "role": "system",
                        "content": f"Jessica transfers the case to {agent_name.upper()}. Reason: {reason}"
                    }
                ]
            }
        )
    
    return handoff


# Create all handoff tools
transfer_to_donna = make_handoff_tool(
    "donna",
    "Send client to Donna for initial intake and fact gathering"
)

transfer_to_mike = make_handoff_tool(
    "mike", 
    "Send to Mike for legal research and precedent search"
)

transfer_to_harvey = make_handoff_tool(
    "harvey",
    "Send to Harvey for case strategy and closing argument"
)

transfer_to_louis = make_handoff_tool(
    "louis",
    "Send to Louis for compliance review and procedural checks"
)

transfer_to_jessica = make_handoff_tool(
    "jessica",
    "Return to Jessica for final decision"
)
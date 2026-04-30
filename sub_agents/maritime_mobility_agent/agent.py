from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import MARITIME_MOBILITY_AGENT_INSTR

maritime_mobility_agent = Agent(
    model="gemini-2.5-flash",
    name="maritime_mobility_agent",
    description=(
        "Maritime mobility specialist: port/shipping-flow monitoring, modernization recommendations, supply-chain memo "
        "drafting, and commerce-disruption alerts."
    ),
    instruction=MARITIME_MOBILITY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

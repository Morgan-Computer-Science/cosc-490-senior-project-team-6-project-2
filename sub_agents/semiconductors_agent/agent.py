from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import SEMICONDUCTORS_AGENT_INSTR

semiconductors_agent = Agent(
    model="gemini-2.5-flash",
    name="semiconductors_agent",
    description=(
        "Semiconductors specialist: chip supply-chain and domestic-capacity monitoring, manufacturing/trade option "
        "recommendations, and disruption alerts."
    ),
    instruction=SEMICONDUCTORS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

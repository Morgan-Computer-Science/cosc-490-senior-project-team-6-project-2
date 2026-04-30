from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import RAIL_AGENT_INSTR

rail_agent = Agent(
    model="gemini-2.5-flash",
    name="rail_agent",
    description=(
        "Rail specialist: freight/passenger performance and expansion monitoring, modernization recommendations, "
        "competitiveness memo drafting, and bottleneck/safety alerts."
    ),
    instruction=RAIL_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import TRANSIT_AGENT_INSTR

transit_agent = Agent(
    model="gemini-2.5-flash",
    name="transit_agent",
    description=(
        "Transit specialist: ridership/safety/reliability/funding-gap monitoring, support strategy recommendations, and "
        "major service-breakdown alerts."
    ),
    instruction=TRANSIT_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

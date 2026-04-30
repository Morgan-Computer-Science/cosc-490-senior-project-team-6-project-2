from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import ALLIANCES_AGENT_INSTR

alliances_agent = Agent(
    model="gemini-2.5-flash",
    name="alliances_agent",
    description=(
        "Alliances specialist: commitment and burden-sharing monitoring, alliance coordination recommendations, and strain/"
        "opportunity briefs with national security coordination."
    ),
    instruction=ALLIANCES_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

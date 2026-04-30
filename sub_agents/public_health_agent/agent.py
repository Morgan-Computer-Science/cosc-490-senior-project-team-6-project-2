from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import PUBLIC_HEALTH_AGENT_INSTR

public_health_agent = Agent(
    model="gemini-2.5-flash",
    name="public_health_agent",
    description=(
        "Public health specialist: outbreaks, mortality, vaccination, and preparedness monitoring with emergency alerts, "
        "rapid response options, and crisis communication support."
    ),
    instruction=PUBLIC_HEALTH_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

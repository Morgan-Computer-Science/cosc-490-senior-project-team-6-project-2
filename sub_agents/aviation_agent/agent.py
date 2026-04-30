from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import AVIATION_AGENT_INSTR

aviation_agent = Agent(
    model="gemini-2.5-flash",
    name="aviation_agent",
    description=(
        "Aviation specialist: air traffic/congestion/safety/airline-strain monitoring, system-improvement recommendations, "
        "briefing-note drafting, and disruption alerts."
    ),
    instruction=AVIATION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

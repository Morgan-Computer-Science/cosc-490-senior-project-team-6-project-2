from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import GRID_RESILIENCE_AGENT_INSTR

grid_resilience_agent = Agent(
    model="gemini-2.5-flash",
    name="grid_resilience_agent",
    description=(
        "Grid resilience specialist: outage and vulnerability monitoring, hardening project options, resilience briefing "
        "drafting, and major threat alerts."
    ),
    instruction=GRID_RESILIENCE_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

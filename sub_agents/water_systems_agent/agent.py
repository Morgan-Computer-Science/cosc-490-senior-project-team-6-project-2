from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import WATER_SYSTEMS_AGENT_INSTR

water_systems_agent = Agent(
    model="gemini-2.5-flash",
    name="water_systems_agent",
    description=(
        "Water systems specialist: water safety, aging pipes, drought stress, wastewater monitoring, resilience planning, "
        "and contamination-risk alerts."
    ),
    instruction=WATER_SYSTEMS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

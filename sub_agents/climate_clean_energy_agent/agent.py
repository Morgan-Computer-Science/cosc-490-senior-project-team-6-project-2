from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import CLIMATE_CLEAN_ENERGY_AGENT_INSTR

climate_clean_energy_agent = Agent(
    model="gemini-2.5-flash",
    name="climate_clean_energy_agent",
    description=(
        "Climate and clean energy specialist: emissions tracking, climate goals, deployment trends, emissions-reduction "
        "pathways, clean-energy investment proposals, and climate emergency alerts."
    ),
    instruction=CLIMATE_CLEAN_ENERGY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

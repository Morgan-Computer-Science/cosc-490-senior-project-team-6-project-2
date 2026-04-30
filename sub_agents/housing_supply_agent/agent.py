from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import HOUSING_SUPPLY_AGENT_INSTR

housing_supply_agent = Agent(
    model="gemini-2.5-flash",
    name="housing_supply_agent",
    description=(
        "Housing supply specialist: permits, construction, zoning barriers, shortages, expansion strategies, and "
        "regional supply-crisis alerting."
    ),
    instruction=HOUSING_SUPPLY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

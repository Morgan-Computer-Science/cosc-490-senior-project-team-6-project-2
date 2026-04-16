from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import COMMODITY_POLICY_AGENT_INSTR

commodity_policy_agent = Agent(
    model="gemini-2.5-flash",
    name="commodity_policy_agent",
    description=(
        "Commodity policy specialist: crop/livestock prices and supply shocks, scenario analysis of tariffs/drought/"
        "subsidies, stabilization options, sector briefings — coordinates conceptually with economic and foreign "
        "relations angles when noted."
    ),
    instruction=COMMODITY_POLICY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

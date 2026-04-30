from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import INFLATION_AGENT_INSTR

inflation_agent = Agent(
    model="gemini-2.5-flash",
    name="inflation_agent",
    description=(
        "Inflation specialist: CPI/PPI, supply chain and input costs, housing and food in aggregate, drivers of price moves, "
        "stabilization options, cost-of-living briefings, coordination with housing, agriculture, transportation; alerts."
    ),
    instruction=INFLATION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

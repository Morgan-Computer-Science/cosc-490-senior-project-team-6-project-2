from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import INSURANCE_MARKETS_AGENT_INSTR

insurance_markets_agent = Agent(
    model="gemini-2.5-flash",
    name="insurance_markets_agent",
    description=(
        "Insurance markets specialist: premiums, insurer participation, competition, exchange stability, and consumer "
        "impact analysis with market-stabilization policy options."
    ),
    instruction=INSURANCE_MARKETS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

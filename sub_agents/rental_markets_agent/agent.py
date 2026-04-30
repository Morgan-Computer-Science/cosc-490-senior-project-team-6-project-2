from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import RENTAL_MARKETS_AGENT_INSTR

rental_markets_agent = Agent(
    model="gemini-2.5-flash",
    name="rental_markets_agent",
    description=(
        "Rental markets specialist: eviction risk, vacancy, rent growth, landlord/tenant trends, renter-protection options, "
        "and high-pressure city/region alerts."
    ),
    instruction=RENTAL_MARKETS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

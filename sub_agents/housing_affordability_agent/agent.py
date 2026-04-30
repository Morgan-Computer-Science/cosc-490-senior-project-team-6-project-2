from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import HOUSING_AFFORDABILITY_AGENT_INSTR

housing_affordability_agent = Agent(
    model="gemini-2.5-flash",
    name="housing_affordability_agent",
    description=(
        "Housing affordability specialist: rent burden, home prices, mortgage stress, wage mismatch, intervention options, "
        "and instability alerts."
    ),
    instruction=HOUSING_AFFORDABILITY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

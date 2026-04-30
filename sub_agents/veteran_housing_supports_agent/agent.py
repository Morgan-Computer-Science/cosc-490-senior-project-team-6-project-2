from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import VETERAN_HOUSING_SUPPORTS_AGENT_INSTR

veteran_housing_supports_agent = Agent(
    model="gemini-2.5-flash",
    name="veteran_housing_supports_agent",
    description=(
        "Veteran housing supports specialist: homelessness/placement/program-success monitoring, targeted intervention "
        "recommendations, and spike alerts."
    ),
    instruction=VETERAN_HOUSING_SUPPORTS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

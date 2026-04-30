from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import REGIONAL_STRATEGY_AGENT_INSTR

regional_strategy_agent = Agent(
    model="gemini-2.5-flash",
    name="regional_strategy_agent",
    description=(
        "Regional strategy specialist: region-specific risk profiles, tailored strategy options, country-cluster "
        "briefings, and regional instability escalation alerts."
    ),
    instruction=REGIONAL_STRATEGY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

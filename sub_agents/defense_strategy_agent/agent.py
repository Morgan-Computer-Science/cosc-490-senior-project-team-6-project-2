from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import DEFENSE_STRATEGY_AGENT_INSTR

defense_strategy_agent = Agent(
    model="gemini-2.5-flash",
    name="defense_strategy_agent",
    description=(
        "Defense strategy specialist: posture/readiness/priority monitoring, strategic briefing drafting, response-option "
        "recommendations, and capability-gap alerts."
    ),
    instruction=DEFENSE_STRATEGY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

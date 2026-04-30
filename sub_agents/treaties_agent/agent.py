from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import TREATIES_AGENT_INSTR

treaties_agent = Agent(
    model="gemini-2.5-flash",
    name="treaties_agent",
    description=(
        "Treaties specialist: treaty negotiation and compliance tracking, language comparison, decision summaries, and "
        "legal/geopolitical risk flags."
    ),
    instruction=TREATIES_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

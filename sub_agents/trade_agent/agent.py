from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import TRADE_AGENT_INSTR

trade_agent = Agent(
    model="gemini-2.5-flash",
    name="trade_agent",
    description=(
        "Trade specialist: imports/exports, tariffs, disputes, strategic sectors, negotiation options, job and price impact, "
        "coordination with foreign relations, technology, and agriculture, trade strategy memos, principal-level alerts."
    ),
    instruction=TRADE_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import MACROECONOMY_AGENT_INSTR

macroeconomy_agent = Agent(
    model="gemini-2.5-flash",
    name="macroeconomy_agent",
    description=(
        "Macroeconomy specialist: GDP, growth, productivity, recession signals, health dashboards, policy risk scenarios, "
        "presidential briefings, principal alerts on acute downturn signals."
    ),
    instruction=MACROECONOMY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

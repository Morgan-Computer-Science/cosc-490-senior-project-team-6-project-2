from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import DIPLOMACY_AGENT_INSTR

diplomacy_agent = Agent(
    model="gemini-2.5-flash",
    name="diplomacy_agent",
    description=(
        "Diplomacy specialist: country/region diplomatic developments, talking points, negotiation priorities, and "
        "escalation alerts coordinated with national security and trade policy."
    ),
    instruction=DIPLOMACY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

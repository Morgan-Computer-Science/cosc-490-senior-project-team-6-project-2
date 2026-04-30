from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import LEGAL_IMMIGRATION_AGENT_INSTR

legal_immigration_agent = Agent(
    model="gemini-2.5-flash",
    name="legal_immigration_agent",
    description=(
        "Legal immigration specialist: visa backlogs, employment pathways, family reunification, process modernization, "
        "and workforce impact monitoring."
    ),
    instruction=LEGAL_IMMIGRATION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

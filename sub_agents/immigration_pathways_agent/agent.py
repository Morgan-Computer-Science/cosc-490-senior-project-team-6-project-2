from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import IMMIGRATION_PATHWAYS_AGENT_INSTR

immigration_pathways_agent = Agent(
    model="gemini-2.5-flash",
    name="immigration_pathways_agent",
    description=(
        "Immigration pathways specialist: legalization/status-adjustment proposal analysis, economic and social outcome "
        "framing, legal-constraint flags, and executive/legislative policy option drafting."
    ),
    instruction=IMMIGRATION_PATHWAYS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

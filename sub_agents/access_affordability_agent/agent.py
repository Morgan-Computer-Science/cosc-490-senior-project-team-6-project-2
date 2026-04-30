from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import ACCESS_AFFORDABILITY_AGENT_INSTR

access_affordability_agent = Agent(
    model="gemini-2.5-flash",
    name="access_affordability_agent",
    description=(
        "Access and affordability specialist: uninsured and provider-shortage monitoring, cost pressure analysis, coverage "
        "expansion options, and underserved-population risk flagging."
    ),
    instruction=ACCESS_AFFORDABILITY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import PUBLIC_LANDS_AGENT_INSTR

public_lands_agent = Agent(
    model="gemini-2.5-flash",
    name="public_lands_agent",
    description=(
        "Public lands specialist: federal land-use and extraction proposals, recreation access, land-management policy "
        "options, and land-use conflict alerts with cross-domain coordination."
    ),
    instruction=PUBLIC_LANDS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

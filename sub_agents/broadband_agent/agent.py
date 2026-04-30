from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import BROADBAND_AGENT_INSTR

broadband_agent = Agent(
    model="gemini-2.5-flash",
    name="broadband_agent",
    description=(
        "Broadband specialist: access-gap and affordability tracking, deployment-progress monitoring, digital-investment "
        "options, and underserved-community alerts."
    ),
    instruction=BROADBAND_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import MILITARY_AFFAIRS_AGENT_INSTR

military_affairs_agent = Agent(
    model="gemini-2.5-flash",
    name="military_affairs_agent",
    description=(
        "Military affairs specialist: personnel/procurement/readiness and force-support tracking, reform options, force "
        "management summaries, and morale/readiness risk alerts."
    ),
    instruction=MILITARY_AFFAIRS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

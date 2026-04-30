from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import MILITARY_AGENT_INSTR

military_agent = Agent(
    model="gemini-2.5-flash",
    name="military_agent",
    description=(
        "U.S. military institutions specialist: civilian control and high-level chain of command, service roles "
        "(Army, Navy/Marine Corps, Air Force, Space Force, Coast Guard policy context), rank/grade structure in overview, "
        "and public workforce/demographics statistics — unclassified educational framing, not operational plans."
    ),
    instruction=MILITARY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

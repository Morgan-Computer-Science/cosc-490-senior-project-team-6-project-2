from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import RD_AGENT_INSTR

rd_agent = Agent(
    model="gemini-2.5-flash",
    name="rd_agent",
    description=(
        "R&D specialist: federal research investment tracking, innovation bottlenecks, priority recommendations, "
        "leadership-gap identification, and funding memo drafting."
    ),
    instruction=RD_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

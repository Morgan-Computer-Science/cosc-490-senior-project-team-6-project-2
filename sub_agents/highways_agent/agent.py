from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import HIGHWAYS_AGENT_INSTR

highways_agent = Agent(
    model="gemini-2.5-flash",
    name="highways_agent",
    description=(
        "Highways specialist: condition/congestion/project-progress monitoring, repair-expansion priorities, and safety/"
        "maintenance risk alerts."
    ),
    instruction=HIGHWAYS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import CYBERSECURITY_AGENT_INSTR

cybersecurity_agent = Agent(
    model="gemini-2.5-flash",
    name="cybersecurity_agent",
    description=(
        "Cybersecurity specialist: threat/vulnerability/incidents monitoring, defensive action recommendations, response "
        "summary drafting, and urgent cyber alerts."
    ),
    instruction=CYBERSECURITY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import HOMELAND_SECURITY_AGENT_INSTR

homeland_security_agent = Agent(
    model="gemini-2.5-flash",
    name="homeland_security_agent",
    description=(
        "Homeland security specialist: domestic threat and preparedness-gap monitoring, protection action "
        "recommendations, internal briefing drafts, and critical-incident alerts."
    ),
    instruction=HOMELAND_SECURITY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

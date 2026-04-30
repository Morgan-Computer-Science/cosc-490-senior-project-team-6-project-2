from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import DETERRENCE_AGENT_INSTR

deterrence_agent = Agent(
    model="gemini-2.5-flash",
    name="deterrence_agent",
    description=(
        "Deterrence specialist: adversary action and deterrence-posture analysis, signaling options, escalation-risk "
        "modeling, and heightened-tension alerts."
    ),
    instruction=DETERRENCE_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

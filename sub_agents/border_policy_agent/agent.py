from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import BORDER_POLICY_AGENT_INSTR

border_policy_agent = Agent(
    model="gemini-2.5-flash",
    name="border_policy_agent",
    description=(
        "Border policy specialist: border activity, processing delays, resource strain, operational adjustment options, "
        "and emergency surge alerts."
    ),
    instruction=BORDER_POLICY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

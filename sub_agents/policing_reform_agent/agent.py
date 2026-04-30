from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import POLICING_REFORM_AGENT_INSTR

policing_reform_agent = Agent(
    model="gemini-2.5-flash",
    name="policing_reform_agent",
    description=(
        "Policing reform specialist: legislation and department reforms, jurisdictional best practices, executive guidance, "
        "use-of-force and accountability metrics, civil rights risk framing — policy only, not case advice."
    ),
    instruction=POLICING_REFORM_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

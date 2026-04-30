from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import PRISONS_REENTRY_AGENT_INSTR

prisons_reentry_agent = Agent(
    model="gemini-2.5-flash",
    name="prisons_reentry_agent",
    description=(
        "Prisons and reentry specialist: incarceration and recidivism data, facility conditions, rehabilitation and reentry, "
        "BOP and federal grant performance, and cross-agency coordination (Labor, Housing, Education) — policy, not case advice."
    ),
    instruction=PRISONS_REENTRY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

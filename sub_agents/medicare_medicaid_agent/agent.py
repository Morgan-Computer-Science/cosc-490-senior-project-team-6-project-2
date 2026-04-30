from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import MEDICARE_MEDICAID_AGENT_INSTR

medicare_medicaid_agent = Agent(
    model="gemini-2.5-flash",
    name="medicare_medicaid_agent",
    description=(
        "Medicare/Medicaid specialist: enrollment and reimbursement analysis, reform summary drafting, budget pressure "
        "flagging, and implementation impact monitoring."
    ),
    instruction=MEDICARE_MEDICAID_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import STUDENT_AID_AGENT_INSTR

student_aid_agent = Agent(
    model="gemini-2.5-flash",
    name="student_aid_agent",
    description=(
        "Student aid specialist: Pell and loan trends, repayment and debt burden, aid reform options, debt-relief scenario "
        "impacts, and implementation/fraud risk flags."
    ),
    instruction=STUDENT_AID_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

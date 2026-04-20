from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import COURTS_SENTENCING_AGENT_INSTR

courts_sentencing_agent = Agent(
    model="gemini-2.5-flash",
    name="courts_sentencing_agent",
    description=(
        "Courts and sentencing specialist: backlogs and disparities, sentencing reform options, justice-impact summaries, "
        "state/federal comparisons — flags principal attention on urgent judicial bottlenecks."
    ),
    instruction=COURTS_SENTENCING_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

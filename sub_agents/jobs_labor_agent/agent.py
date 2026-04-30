from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import JOBS_LABOR_AGENT_INSTR

jobs_labor_agent = Agent(
    model="gemini-2.5-flash",
    name="jobs_labor_agent",
    description=(
        "Jobs and labor specialist: unemployment, participation, wages, sector trends, workforce initiatives, disruption "
        "scenarios by industry, memos; coordination notes for education and technology; principal alerts on acute stress."
    ),
    instruction=JOBS_LABOR_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import K12_AGENT_INSTR

k12_agent = Agent(
    model="gemini-2.5-flash",
    name="k12_agent",
    description=(
        "K-12 education specialist: school performance, attendance, literacy, and funding gaps; federal initiative options; "
        "support planning for underperforming districts; and student wellbeing coordination themes."
    ),
    instruction=K12_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

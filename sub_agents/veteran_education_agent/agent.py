from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import VETERAN_EDUCATION_AGENT_INSTR

veteran_education_agent = Agent(
    model="gemini-2.5-flash",
    name="veteran_education_agent",
    description=(
        "Veteran education specialist: GI Bill usage/completion/access-barrier monitoring, support-improvement options, "
        "opportunity briefing drafting, and institutional-access alerts."
    ),
    instruction=VETERAN_EDUCATION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

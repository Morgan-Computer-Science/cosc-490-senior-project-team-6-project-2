from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import VETERAN_EMPLOYMENT_AGENT_INSTR

veteran_employment_agent = Agent(
    model="gemini-2.5-flash",
    name="veteran_employment_agent",
    description=(
        "Veteran employment specialist: unemployment/placement/skills-transition tracking, workforce initiative "
        "recommendations, and hiring/retraining strategy memos."
    ),
    instruction=VETERAN_EMPLOYMENT_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

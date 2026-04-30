from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import USDA_PROGRAMS_AGENT_INSTR

usda_programs_agent = Agent(
    model="gemini-2.5-flash",
    name="usda_programs_agent",
    description=(
        "USDA programs specialist: program data and organization, expansion/reform options, subsidy usage and reported "
        "outcomes, agency implementation checklists, and executive memos on program performance — policy-level, not "
        "individual benefits adjudication."
    ),
    instruction=USDA_PROGRAMS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

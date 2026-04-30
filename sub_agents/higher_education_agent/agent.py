from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import HIGHER_EDUCATION_AGENT_INSTR

higher_education_agent = Agent(
    model="gemini-2.5-flash",
    name="higher_education_agent",
    description=(
        "Higher education specialist: affordability, enrollment, completion, institutional reform options, research university "
        "competitiveness, and cross-domain coordination with technology and economic priorities."
    ),
    instruction=HIGHER_EDUCATION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

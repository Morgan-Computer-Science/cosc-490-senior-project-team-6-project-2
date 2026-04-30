from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import MILITARY_FAMILIES_AGENT_INSTR

military_families_agent = Agent(
    model="gemini-2.5-flash",
    name="military_families_agent",
    description=(
        "Military families specialist: childcare/spouse-employment/relocation/wellbeing monitoring, support-policy "
        "recommendations, quality-of-life memo drafting, and major support-gap alerts."
    ),
    instruction=MILITARY_FAMILIES_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

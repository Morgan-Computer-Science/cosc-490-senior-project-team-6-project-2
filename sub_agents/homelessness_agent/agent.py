from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import HOMELESSNESS_AGENT_INSTR

homelessness_agent = Agent(
    model="gemini-2.5-flash",
    name="homelessness_agent",
    description=(
        "Homelessness specialist: shelter capacity, unsheltered counts, supportive-service gaps, emergency interventions, "
        "and humanitarian alerting."
    ),
    instruction=HOMELESSNESS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

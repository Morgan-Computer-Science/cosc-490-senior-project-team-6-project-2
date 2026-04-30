from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import FAIR_HOUSING_AGENT_INSTR

fair_housing_agent = Agent(
    model="gemini-2.5-flash",
    name="fair_housing_agent",
    description=(
        "Fair housing specialist: discrimination and enforcement patterns, civil rights policy options, equitable-access "
        "trend monitoring, and coordination with justice/HUD-like workflows."
    ),
    instruction=FAIR_HOUSING_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

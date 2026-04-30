from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import FOOD_SECURITY_AGENT_INSTR

food_security_agent = Agent(
    model="gemini-2.5-flash",
    name="food_security_agent",
    description=(
        "Food security specialist: hunger and food access indicators, SNAP and school meals policy, hotspot-style "
        "assessment, emergency assistance options, crisis memos — flags principal-level attention when shortages or "
        "hardship worsen."
    ),
    instruction=FOOD_SECURITY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

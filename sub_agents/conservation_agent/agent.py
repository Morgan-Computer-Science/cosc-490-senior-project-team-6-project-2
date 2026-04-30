from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import CONSERVATION_AGENT_INSTR

conservation_agent = Agent(
    model="gemini-2.5-flash",
    name="conservation_agent",
    description=(
        "Conservation specialist: biodiversity, forests, wetlands, habitat preservation actions, initiative memos, "
        "conservation funding tracking, and coordination with agriculture/public lands themes."
    ),
    instruction=CONSERVATION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

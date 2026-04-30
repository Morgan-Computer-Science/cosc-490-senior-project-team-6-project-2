from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import HUMANITARIAN_PROCESSING_AGENT_INSTR

humanitarian_processing_agent = Agent(
    model="gemini-2.5-flash",
    name="humanitarian_processing_agent",
    description=(
        "Humanitarian processing specialist: asylum/refugee/parole flow tracking, humanitarian capacity options, emergency "
        "protection recommendations, and bottleneck alerts."
    ),
    instruction=HUMANITARIAN_PROCESSING_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

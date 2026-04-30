from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import DIGITAL_COMPETITIVENESS_AGENT_INSTR

digital_competitiveness_agent = Agent(
    model="gemini-2.5-flash",
    name="digital_competitiveness_agent",
    description=(
        "Digital competitiveness specialist: digital-infrastructure and adoption tracking, competitiveness initiative "
        "recommendations, strategic digital-economy summaries, and capability-gap identification."
    ),
    instruction=DIGITAL_COMPETITIVENESS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

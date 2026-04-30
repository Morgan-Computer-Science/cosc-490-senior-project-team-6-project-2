from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import AI_INNOVATION_AGENT_INSTR

ai_innovation_agent = Agent(
    model="gemini-2.5-flash",
    name="ai_innovation_agent",
    description=(
        "AI and innovation specialist: frontier AI capabilities/governance, competitiveness priorities, executive guidance, "
        "and strategic AI risk flags."
    ),
    instruction=AI_INNOVATION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

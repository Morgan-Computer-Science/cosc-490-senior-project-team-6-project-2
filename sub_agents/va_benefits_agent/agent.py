from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import VA_BENEFITS_AGENT_INSTR

va_benefits_agent = Agent(
    model="gemini-2.5-flash",
    name="va_benefits_agent",
    description=(
        "VA benefits specialist: claims/appeals processing monitoring, modernization recommendations, performance memo "
        "drafting, and service-backlog alerts."
    ),
    instruction=VA_BENEFITS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

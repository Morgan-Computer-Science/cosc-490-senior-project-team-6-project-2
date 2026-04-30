from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import WORKFORCE_PATHWAYS_AGENT_INSTR

workforce_pathways_agent = Agent(
    model="gemini-2.5-flash",
    name="workforce_pathways_agent",
    description=(
        "Workforce pathways specialist: apprenticeships, certifications, career pipelines, training gaps, and education-to-"
        "employment planning coordinated with labor, technology, and infrastructure priorities."
    ),
    instruction=WORKFORCE_PATHWAYS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

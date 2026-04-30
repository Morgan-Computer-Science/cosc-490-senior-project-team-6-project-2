from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import PUBLIC_WORKS_AGENT_INSTR

public_works_agent = Agent(
    model="gemini-2.5-flash",
    name="public_works_agent",
    description=(
        "Public works specialist: project timeline/cost tracking, prioritization options, implementation dashboard drafts, "
        "and procurement/execution risk flags."
    ),
    instruction=PUBLIC_WORKS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import DOT_PROGRAMS_AGENT_INSTR

dot_programs_agent = Agent(
    model="gemini-2.5-flash",
    name="dot_programs_agent",
    description=(
        "DOT programs specialist: funding/performance monitoring, implementation audit framing, reform/reallocation "
        "recommendations, and ineffective-program flags."
    ),
    instruction=DOT_PROGRAMS_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

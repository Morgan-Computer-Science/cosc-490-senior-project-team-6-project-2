from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import EPA_POLICY_AGENT_INSTR

epa_policy_agent = Agent(
    model="gemini-2.5-flash",
    name="epa_policy_agent",
    description=(
        "EPA policy specialist: environmental regulation and enforcement tracking, compliance trend analysis, regulatory "
        "action options, pollution/enforcement summaries, and legal or implementation risk flags."
    ),
    instruction=EPA_POLICY_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

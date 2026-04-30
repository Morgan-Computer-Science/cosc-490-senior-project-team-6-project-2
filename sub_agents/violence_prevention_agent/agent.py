from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import VIOLENCE_PREVENTION_AGENT_INSTR

violence_prevention_agent = Agent(
    model="gemini-2.5-flash",
    name="violence_prevention_agent",
    description=(
        "Violence prevention specialist: hotspot and risk-pattern analysis, evidence-based intervention investments, "
        "prevention program design, and cross-sector coordination (education, housing, healthcare) — with urgent alerts on spikes."
    ),
    instruction=VIOLENCE_PREVENTION_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import FARM_BILL_AGENT_INSTR

farm_bill_agent = Agent(
    model="gemini-2.5-flash",
    name="farm_bill_agent",
    description=(
        "Farm Bill legislative specialist: titles and deadlines, amendments and conference dynamics, comparisons to "
        "prior bill language, presidential policy briefs, and impacts on budget, nutrition/food titles, and rural "
        "development — policy-level, not private legal advice."
    ),
    instruction=FARM_BILL_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

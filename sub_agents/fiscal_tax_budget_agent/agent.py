from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool

from .prompt import FISCAL_TAX_BUDGET_AGENT_INSTR

fiscal_tax_budget_agent = Agent(
    model="gemini-2.5-flash",
    name="fiscal_tax_budget_agent",
    description=(
        "Fiscal/tax/budget specialist: tax and spending analysis, deficit and revenue effects, budget tradeoffs, options "
        "memos, flagging unsustainable or risky proposals, principal attention on fiscal stress."
    ),
    instruction=FISCAL_TAX_BUDGET_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

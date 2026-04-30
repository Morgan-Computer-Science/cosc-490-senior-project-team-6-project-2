from google.adk.agents.llm_agent import Agent
from sub_agents.fiscal_tax_budget_agent import fiscal_tax_budget_agent
from sub_agents.inflation_agent import inflation_agent
from sub_agents.jobs_labor_agent import jobs_labor_agent
from sub_agents.macroeconomy_agent import macroeconomy_agent
from sub_agents.trade_agent import trade_agent

from .prompt import ECONOMIC_AGENT_INSTR

economic_agent = Agent(
    model="gemini-2.5-flash",
    name="economic_agent",
    description=(
        "Economic coordinator: routes macroeconomy (macroeconomy_agent), jobs and labor (jobs_labor_agent), inflation "
        "(inflation_agent), fiscal/tax/budget (fiscal_tax_budget_agent), and trade (trade_agent); frames mixed economic asks."
    ),
    instruction=ECONOMIC_AGENT_INSTR,
    tools=[],
    sub_agents=[
        macroeconomy_agent,
        jobs_labor_agent,
        inflation_agent,
        fiscal_tax_budget_agent,
        trade_agent,
    ],
)

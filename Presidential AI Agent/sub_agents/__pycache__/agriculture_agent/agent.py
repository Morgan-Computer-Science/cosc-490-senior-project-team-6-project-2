from google.adk.agents.llm_agent import Agent
from sub_agents.commodity_policy_agent import commodity_policy_agent
from sub_agents.farm_bill_agent import farm_bill_agent
from sub_agents.food_security_agent import food_security_agent
from sub_agents.usda_programs_agent import usda_programs_agent

from .prompt import AGRICULTURE_AGENT_INSTR

agriculture_agent = Agent(
    model="gemini-2.5-flash",
    name="agriculture_agent",
    description=(
        "Agriculture coordinator for the Office: routes Farm Bill (farm_bill_agent), USDA programs (usda_programs_agent), "
        "food security (food_security_agent), and commodity/sector markets (commodity_policy_agent)."
    ),
    instruction=AGRICULTURE_AGENT_INSTR,
    tools=[],
    sub_agents=[farm_bill_agent, usda_programs_agent, food_security_agent, commodity_policy_agent],
)

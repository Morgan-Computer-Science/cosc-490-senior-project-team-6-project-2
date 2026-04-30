from google.adk.agents.llm_agent import Agent
from sub_agents.fair_housing_agent import fair_housing_agent
from sub_agents.homelessness_agent import homelessness_agent
from sub_agents.housing_affordability_agent import housing_affordability_agent
from sub_agents.housing_supply_agent import housing_supply_agent
from sub_agents.rental_markets_agent import rental_markets_agent

from .prompt import HOUSING_AGENT_INSTR

housing_agent = Agent(
    model="gemini-2.5-flash",
    name="housing_agent",
    description=(
        "Housing coordinator: routes housing supply (housing_supply_agent), affordability "
        "(housing_affordability_agent), fair housing (fair_housing_agent), rental markets "
        "(rental_markets_agent), and homelessness (homelessness_agent); handles mixed housing asks."
    ),
    instruction=HOUSING_AGENT_INSTR,
    tools=[],
    sub_agents=[
        housing_supply_agent,
        housing_affordability_agent,
        fair_housing_agent,
        rental_markets_agent,
        homelessness_agent,
    ],
)

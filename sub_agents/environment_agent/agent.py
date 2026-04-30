from google.adk.agents.llm_agent import Agent
from sub_agents.climate_clean_energy_agent import climate_clean_energy_agent
from sub_agents.conservation_agent import conservation_agent
from sub_agents.epa_policy_agent import epa_policy_agent
from sub_agents.public_lands_agent import public_lands_agent

from .prompt import ENVIRONMENT_AGENT_INSTR

environment_agent = Agent(
    model="gemini-2.5-flash",
    name="environment_agent",
    description=(
        "Environment coordinator: routes climate/clean energy (climate_clean_energy_agent), conservation "
        "(conservation_agent), EPA policy (epa_policy_agent), and public lands (public_lands_agent); frames mixed "
        "environment asks when split is unclear."
    ),
    instruction=ENVIRONMENT_AGENT_INSTR,
    tools=[],
    sub_agents=[
        climate_clean_energy_agent,
        conservation_agent,
        epa_policy_agent,
        public_lands_agent,
    ],
)

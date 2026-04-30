from google.adk.agents.llm_agent import Agent
from sub_agents.broadband_agent import broadband_agent
from sub_agents.grid_resilience_agent import grid_resilience_agent
from sub_agents.public_works_agent import public_works_agent
from sub_agents.water_systems_agent import water_systems_agent

from .prompt import INFRASTRUCTURE_AGENT_INSTR

infrastructure_agent = Agent(
    model="gemini-2.5-flash",
    name="infrastructure_agent",
    description=(
        "Infrastructure coordinator: routes water systems (water_systems_agent), grid resilience "
        "(grid_resilience_agent), public works (public_works_agent), and broadband (broadband_agent); handles blended "
        "infrastructure policy asks."
    ),
    instruction=INFRASTRUCTURE_AGENT_INSTR,
    tools=[],
    sub_agents=[water_systems_agent, grid_resilience_agent, public_works_agent, broadband_agent],
)

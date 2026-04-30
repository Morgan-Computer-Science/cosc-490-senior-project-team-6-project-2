from google.adk.agents.llm_agent import Agent
from sub_agents.aviation_agent import aviation_agent
from sub_agents.dot_programs_agent import dot_programs_agent
from sub_agents.highways_agent import highways_agent
from sub_agents.maritime_mobility_agent import maritime_mobility_agent
from sub_agents.rail_agent import rail_agent
from sub_agents.transit_agent import transit_agent

from .prompt import TRANSPORTATION_AGENT_INSTR

transportation_agent = Agent(
    model="gemini-2.5-flash",
    name="transportation_agent",
    description=(
        "Transportation coordinator: routes highways (highways_agent), transit (transit_agent), rail (rail_agent), "
        "aviation (aviation_agent), maritime mobility (maritime_mobility_agent), and DOT programs "
        "(dot_programs_agent); handles mixed transportation asks."
    ),
    instruction=TRANSPORTATION_AGENT_INSTR,
    tools=[],
    sub_agents=[
        highways_agent,
        transit_agent,
        rail_agent,
        aviation_agent,
        maritime_mobility_agent,
        dot_programs_agent,
    ],
)

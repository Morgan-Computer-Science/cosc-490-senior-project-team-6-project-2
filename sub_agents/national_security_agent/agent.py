from google.adk.agents.llm_agent import Agent
from sub_agents.defense_strategy_agent import defense_strategy_agent
from sub_agents.deterrence_agent import deterrence_agent
from sub_agents.homeland_security_agent import homeland_security_agent
from sub_agents.military_affairs_agent import military_affairs_agent

from .prompt import NATIONAL_SECURITY_AGENT_INSTR

national_security_agent = Agent(
    model="gemini-2.5-flash",
    name="national_security_agent",
    description=(
        "National security coordinator: routes defense strategy (defense_strategy_agent), deterrence "
        "(deterrence_agent), homeland security (homeland_security_agent), and military affairs "
        "(military_affairs_agent); handles blended national-security asks."
    ),
    instruction=NATIONAL_SECURITY_AGENT_INSTR,
    tools=[],
    sub_agents=[
        defense_strategy_agent,
        deterrence_agent,
        homeland_security_agent,
        military_affairs_agent,
    ],
)

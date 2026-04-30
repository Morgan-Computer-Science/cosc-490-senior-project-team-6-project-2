from google.adk.agents.llm_agent import Agent
from sub_agents.alliances_agent import alliances_agent
from sub_agents.diplomacy_agent import diplomacy_agent
from sub_agents.regional_strategy_agent import regional_strategy_agent
from sub_agents.treaties_agent import treaties_agent

from .prompt import FOREIGN_RELATIONS_AGENT_INSTR

foreign_relations_agent = Agent(
    model="gemini-2.5-flash",
    name="foreign_relations_agent",
    description=(
        "Foreign relations coordinator: routes diplomacy (diplomacy_agent), treaties (treaties_agent), alliances "
        "(alliances_agent), and regional strategy (regional_strategy_agent); handles blended foreign policy asks."
    ),
    instruction=FOREIGN_RELATIONS_AGENT_INSTR,
    tools=[],
    sub_agents=[diplomacy_agent, treaties_agent, alliances_agent, regional_strategy_agent],
)

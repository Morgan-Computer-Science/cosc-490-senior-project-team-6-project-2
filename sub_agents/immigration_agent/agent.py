from google.adk.agents.llm_agent import Agent
from sub_agents.border_policy_agent import border_policy_agent
from sub_agents.humanitarian_processing_agent import humanitarian_processing_agent
from sub_agents.immigration_pathways_agent import immigration_pathways_agent
from sub_agents.legal_immigration_agent import legal_immigration_agent

from .prompt import IMMIGRATION_AGENT_INSTR

immigration_agent = Agent(
    model="gemini-2.5-flash",
    name="immigration_agent",
    description=(
        "Immigration coordinator: routes border policy (border_policy_agent), legal immigration "
        "(legal_immigration_agent), pathways/status adjustment (immigration_pathways_agent), and humanitarian "
        "processing (humanitarian_processing_agent); handles mixed immigration asks."
    ),
    instruction=IMMIGRATION_AGENT_INSTR,
    tools=[],
    sub_agents=[
        border_policy_agent,
        legal_immigration_agent,
        immigration_pathways_agent,
        humanitarian_processing_agent,
    ],
)

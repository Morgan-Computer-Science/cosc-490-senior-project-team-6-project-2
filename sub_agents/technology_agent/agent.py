from google.adk.agents.llm_agent import Agent
from sub_agents.ai_innovation_agent import ai_innovation_agent
from sub_agents.cybersecurity_agent import cybersecurity_agent
from sub_agents.digital_competitiveness_agent import digital_competitiveness_agent
from sub_agents.rd_agent import rd_agent
from sub_agents.semiconductors_agent import semiconductors_agent

from .prompt import TECHNOLOGY_AGENT_INSTR

technology_agent = Agent(
    model="gemini-2.5-flash",
    name="technology_agent",
    description=(
        "Technology coordinator: routes AI/innovation (ai_innovation_agent), cybersecurity (cybersecurity_agent), "
        "R&D (rd_agent), semiconductors (semiconductors_agent), and digital competitiveness "
        "(digital_competitiveness_agent); handles mixed technology asks."
    ),
    instruction=TECHNOLOGY_AGENT_INSTR,
    tools=[],
    sub_agents=[
        ai_innovation_agent,
        cybersecurity_agent,
        rd_agent,
        semiconductors_agent,
        digital_competitiveness_agent,
    ],
)

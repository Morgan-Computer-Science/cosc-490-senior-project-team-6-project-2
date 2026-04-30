from google.adk.agents.llm_agent import Agent
from sub_agents.access_affordability_agent import access_affordability_agent
from sub_agents.insurance_markets_agent import insurance_markets_agent
from sub_agents.medicare_medicaid_agent import medicare_medicaid_agent
from sub_agents.public_health_agent import public_health_agent

from .prompt import HEALTHCARE_AGENT_INSTR

healthcare_agent = Agent(
    model="gemini-2.5-flash",
    name="healthcare_agent",
    description=(
        "Healthcare coordinator: routes access/affordability (access_affordability_agent), Medicare/Medicaid "
        "(medicare_medicaid_agent), public health (public_health_agent), and insurance markets "
        "(insurance_markets_agent); handles mixed healthcare policy asks."
    ),
    instruction=HEALTHCARE_AGENT_INSTR,
    tools=[],
    sub_agents=[
        access_affordability_agent,
        medicare_medicaid_agent,
        public_health_agent,
        insurance_markets_agent,
    ],
)

from google.adk.agents.llm_agent import Agent
from sub_agents.military_families_agent import military_families_agent
from sub_agents.va_benefits_agent import va_benefits_agent
from sub_agents.veteran_education_agent import veteran_education_agent
from sub_agents.veteran_employment_agent import veteran_employment_agent
from sub_agents.veteran_housing_supports_agent import veteran_housing_supports_agent

from .prompt import VETERANS_AGENT_INSTR

veterans_agent = Agent(
    model="gemini-2.5-flash",
    name="veterans_agent",
    description=(
        "Veterans coordinator: routes VA benefits (va_benefits_agent), veteran education "
        "(veteran_education_agent), veteran employment (veteran_employment_agent), veteran housing supports "
        "(veteran_housing_supports_agent), and military families (military_families_agent); handles mixed veterans asks."
    ),
    instruction=VETERANS_AGENT_INSTR,
    tools=[],
    sub_agents=[
        va_benefits_agent,
        veteran_education_agent,
        veteran_employment_agent,
        veteran_housing_supports_agent,
        military_families_agent,
    ],
)

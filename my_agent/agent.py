from google.adk.agents.llm_agent import Agent
from sub_agents.agriculture_agent import agriculture_agent
from sub_agents.criminal_justice_agent import criminal_justice_agent
from sub_agents.economic_agent import economic_agent
from sub_agents.education_agent import education_agent
from sub_agents.environment_agent import environment_agent
from sub_agents.foreign_relations_agent import foreign_relations_agent
from sub_agents.healthcare_agent import healthcare_agent
from sub_agents.housing_agent import housing_agent
from sub_agents.immigration_agent import immigration_agent
from sub_agents.infrastructure_agent import infrastructure_agent
from sub_agents.military_agent import military_agent
from sub_agents.national_security_agent import national_security_agent
from sub_agents.technology_agent import technology_agent
from sub_agents.transportation_agent import transportation_agent
from sub_agents.veterans_agent import veterans_agent

from .prompt import ROOT_AGENT_INSTR


def get_current_time(city: str) -> dict:
    return {"status": "success", "city": city, "time": "10:30 AM"}


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description=(
        "Principal Office assistant for U.S. presidential leadership and policy; coordinates specialist sub-agents "
        "(economy—macro, jobs, inflation, fiscal/tax/budget, and trade; environment, technology, national security, education, "
        "healthcare, infrastructure, immigration, "
        "criminal justice—including policing, courts/sentencing, prisons/reentry, and violence prevention—housing, "
        "veterans, agriculture, transportation, foreign relations)."
    ),
    instruction=ROOT_AGENT_INSTR,
    # No tools here: Gemini disallows mixing built-in google_search with agent transfer (function calling).
    # Web search runs on leaf specialists only. Transfer uses function calling on the root.
    tools=[],
    sub_agents=[
        agriculture_agent,
        criminal_justice_agent,
        economic_agent,
        education_agent,
        environment_agent,
        foreign_relations_agent,
        healthcare_agent,
        housing_agent,
        immigration_agent,
        infrastructure_agent,
        military_agent,
        national_security_agent,
        technology_agent,
        transportation_agent,
        veterans_agent,
    ],
)

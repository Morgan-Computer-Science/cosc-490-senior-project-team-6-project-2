from agents.health_agent import HealthPolicyAgent
from agents.labor_agent import EmploymentLaborAgent
from agents.environmental_agent import EnvironmentalPolicyAgent
from agents.technological_agent import TechnologicalPolicyAgent
from agents.technological_agent import HousingAgent
from agents.technological_agent import EducationAgent
from agents.technological_agent import NationalSecurityAgent
from agents.technological_agent import Econmonic Agent
def run_agents(scenario):

    agents = [
        HealthPolicyAgent(),
        EmploymentLaborAgent(),
        EnvironmentalPolicyAgent(),
        TechnologicalPolicyAgent(),
        HousingAgent(),
        EducationAgent(),
        NationalSecurityAgent(),
        EconomicAgent()
    ]

    results = {}

    for agent in agents:
        results[agent.name] = agent.run(scenario)

    return results

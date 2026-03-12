from agents.health_agent import HealthPolicyAgent
from agents.labor_agent import EmploymentLaborAgent
from agents.environmental_agent import EnvironmentalPolicyAgent
from agents.technological_agent import TechnologicalPolicyAgent
def run_agents(scenario):

    agents = [
        HealthPolicyAgent(),
        EmploymentLaborAgent(),
        EnvironmentalPolicyAgent(),
        TechnologicalPolicyAgent(),
        HousingAgent(),
        EducationAgent(),
        NationalSecurityAgent()
    ]

    results = {}

    for agent in agents:
        results[agent.name] = agent.run(scenario)

    return results

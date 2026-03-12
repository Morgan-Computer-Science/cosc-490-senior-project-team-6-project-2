from agents.health_agent import HealthPolicyAgent
from agents.labor_agent import EmploymentLaborAgent
from agents.environmental_agent import EnvironmentalPolicyAgent
from agents.technological_agent import TechnologicalPolicyAgent
def run_agents(scenario):

    agents = [
        HealthPolicyAgent(),
        EmploymentLaborAgent(),
        EnvironmentalPolicyAgent(),
        TechnologicalPolicyAgent()
    ]

    results = {}

    for agent in agents:
        results[agent.name] = agent.analyze(scenario)

    return results

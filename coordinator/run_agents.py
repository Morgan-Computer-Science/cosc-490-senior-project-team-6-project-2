from agents.health_agent import HealthPolicyAgent
from agents.labor_agent import EmploymentLaborAgent

def run_agents(scenario):

    agents = [
        HealthPolicyAgent(),
        EmploymentLaborAgent()
    ]

    results = {}

    for agent in agents:
        results[agent.name] = agent.analyze(scenario)

    return results

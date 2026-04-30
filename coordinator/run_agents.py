from agents.health_agent import HealthPolicyAgent
from agents.labor_agent import EmploymentLaborAgent
from agents.environmental_agent import EnvironmentalPolicyAgent
from agents.technological_agent import TechnologicalPolicyAgent
#from agents.housing_agent import HousingAgent
#from agents.education_agent import EducationAgent
#from agents.national_security_agent import NationalSecurityAgent
#from agents.economic_agent import EconmonicAgent
def run_agents(scenario):

    agents = [
        HealthPolicyAgent(),
        EmploymentLaborAgent(),
        EnvironmentalPolicyAgent(),
        TechnologicalPolicyAgent(),
    
    ]

    results = {}

    for agent in agents:
        results[agent.name] = agent.run(scenario)

    return results

from google.adk.agents.llm_agent import Agent
from sub_agents.courts_sentencing_agent import courts_sentencing_agent
from sub_agents.policing_reform_agent import policing_reform_agent
from sub_agents.prisons_reentry_agent import prisons_reentry_agent
from sub_agents.violence_prevention_agent import violence_prevention_agent

from .prompt import CRIMINAL_JUSTICE_AGENT_INSTR

criminal_justice_agent = Agent(
    model="gemini-2.5-flash",
    name="criminal_justice_agent",
    description=(
        "Criminal justice coordinator: routes policing reform (policing_reform_agent), courts/sentencing "
        "(courts_sentencing_agent), prisons and reentry (prisons_reentry_agent), and violence prevention "
        "(violence_prevention_agent); frames cross-cutting justice questions when the split is unclear."
    ),
    instruction=CRIMINAL_JUSTICE_AGENT_INSTR,
    tools=[],
    sub_agents=[
        policing_reform_agent,
        courts_sentencing_agent,
        prisons_reentry_agent,
        violence_prevention_agent,
    ],
)

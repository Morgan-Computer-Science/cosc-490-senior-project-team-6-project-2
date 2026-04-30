from google.adk.agents.llm_agent import Agent
from sub_agents.courts_sentencing_agent import courts_sentencing_agent
from sub_agents.policing_reform_agent import policing_reform_agent

from .prompt import CRIMINAL_JUSTICE_AGENT_INSTR

criminal_justice_agent = Agent(
    model="gemini-2.5-flash",
    name="criminal_justice_agent",
    description=(
        "Criminal justice coordinator: routes policing reform (policing_reform_agent) and courts/sentencing "
        "(courts_sentencing_agent); handles cross-cutting justice framing when the split is unclear."
    ),
    instruction=CRIMINAL_JUSTICE_AGENT_INSTR,
    tools=[],
    sub_agents=[policing_reform_agent, courts_sentencing_agent],
)

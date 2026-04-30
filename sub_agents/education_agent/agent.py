from google.adk.agents.llm_agent import Agent
from sub_agents.higher_education_agent import higher_education_agent
from sub_agents.k12_agent import k12_agent
from sub_agents.student_aid_agent import student_aid_agent
from sub_agents.workforce_pathways_agent import workforce_pathways_agent

from .prompt import EDUCATION_AGENT_INSTR

education_agent = Agent(
    model="gemini-2.5-flash",
    name="education_agent",
    description=(
        "Education coordinator: routes K-12 (k12_agent), higher education (higher_education_agent), student aid "
        "(student_aid_agent), and workforce pathways (workforce_pathways_agent); frames mixed education policy asks."
    ),
    instruction=EDUCATION_AGENT_INSTR,
    tools=[],
    sub_agents=[
        k12_agent,
        higher_education_agent,
        student_aid_agent,
        workforce_pathways_agent,
    ],
)

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from .prompt import ROOT_AGENT_INSTR
from Education.workforce_agent import workforce_agent
from Education.policy_agent import policy_agent



def get_current_time(city: str) -> dict:
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="AI advisor for U.S. education policy at the presidential level",
    instruction=ROOT_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    sub_agents=[policy_agent, workforce_agent],
)
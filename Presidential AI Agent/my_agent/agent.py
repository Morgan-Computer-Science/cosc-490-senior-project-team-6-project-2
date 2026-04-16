from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from .prompt import ROOT_AGENT_INSTR
from sub_agents.labor_agent import labor_agent
from sub_agents.economic_agent import economic_agent

def get_current_time(city: str) -> dict:
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for Political Leadership questions.',
    instruction=ROOT_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    sub_agents=[ labor_agent,
    economic_agent],
)

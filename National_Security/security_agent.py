from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from .prompt import ROOT_AGENT_INSTR
from National_Security.cyber_agent import cyber_agent
from National_Security.geo_agent import geo_agent


def get_current_time(city: str) -> dict:
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="AI advisor for U.S. national security policy at the presidential level",
    instruction=ROOT_AGENT_INSTR,
    tools=[GoogleSearchTool()],
    sub_agents=[geo_agent, cyber_agent],
)
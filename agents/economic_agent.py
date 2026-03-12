from agents.base_agent import BaseAgent

class EconomicAgent(BasePolicyAgent):
    def __init__(self):
        super().__init__(
            name="Economic Agent",
            prompt = "prompts/economic.txt"
        )
from agents.base_agent import BasePolicyAgent

class HousingAgent(BasePolicyAgent):
    def __init__(self):
        super().__init__(
            name="Housing Agent",
            prompt = "prompts/housing.txt"
        )
from agents.base_agent import BasePolicyAgent

class EnvironmentalPolicyAgent(BasePolicyAgent):
    def __init__(self):
        super().__init__(
            name="Environmental Policy Agent",
            prompt_file="prompts/environmental_sustainability.txt",
        )

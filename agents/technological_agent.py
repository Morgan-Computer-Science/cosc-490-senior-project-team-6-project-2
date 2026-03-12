from agents.base_agent import BasePolicyAgent

class TechnologicalPolicyAgent(BasePolicyAgent):
    def __init__(self):
        super().__init__(
            name="Technological Policy Agent",
            prompt_file="prompts/technological_advancement.txt",
        )
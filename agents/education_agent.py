from agents.base_agent import BasePolicyAgent

class EducationAgent(BasePolicyAgent):
    def __init__(self):
        super().__init__(
            name="Education Agent",
            prompt_file="prompts/education_prompt.txt",
        )
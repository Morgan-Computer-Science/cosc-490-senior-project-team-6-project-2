from agents.base_agent import BasePolicyAgent

class EmploymentLaborAgent(BasePolicyAgent):
    def __init__(self):
        super().__init__(
            name="Employment & Labor Agent",
            prompt_file="prompts/employment_labor.txt",
        )

from agents.base_agent import BasePolicyAgent

class HealthPolicyAgent(BasePolicyAgent):
    def __init__(self):
        super().__init__(
            name="Health Policy Agent",
            prompt_file="prompts/health_policy.txt",
        )

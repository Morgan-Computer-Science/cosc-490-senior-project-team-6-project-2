from pathlib import Path
from google import genai

class BasePolicyAgent:
    def __init__(self, name: str, prompt_file: str, model: str = "gemini-2.5-flash"):
        self.name = name
        self.model = model
        self.prompt_text = Path(prompt_file).read_text(encoding="utf-8")
        self.client = genai.Client(api_key="AIzaSyDgo0Tpl_MlkxelgJRz9n1KQIrL_Rz-iNY")

    def analyze(self, scenario: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"Scenario:\n{scenario}",
            config={
                "system_instruction": self.prompt_text,
                "temperature": 0.4,
            },
        )
        return response.text.strip()



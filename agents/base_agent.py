import google.generativeai as genai
import os


class BasePolicyAgent:

    def __init__(self, name, prompt_file):

        self.name = name
        self.prompt_file = prompt_file

        genai.configure(api_key=os.getenv("AIzaSyDgo0Tpl_MlkxelgJRz9n1KQIrL_Rz-iNY"))

        with open(prompt_file, "r") as f:
            self.system_prompt = f.read()

        self.model = genai.GenerativeModel("gemini-1.5-flash")


    def run(self, scenario):

        prompt = f"""
{self.system_prompt}

SCENARIO:
{scenario}
"""

        response = self.model.generate_content(prompt)

        return response.text



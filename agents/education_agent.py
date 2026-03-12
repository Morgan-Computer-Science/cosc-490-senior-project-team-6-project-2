# education_advisor_agent.py

import os
import vertexai
from vertexai.generative_models import GenerativeModel

os.environ["PROJECT"] = "capstone-490018"

api_key = os.environ.get("Key")
if not api_key:
    raise EnvironmentError("Key environment variable not set.")

vertexai.init(
    project="capstone-490018",
    location="us-central1",
    api_key=api_key
)

# Load Gemini model
model = GenerativeModel("gemini-2.0-flash-001")

SYSTEM_PROMPT = """
You are the Presidential Advisor for Education.

Your responsibilities:
- analyze education policy
- evaluate national education data
- recommend federal policy actions
- prepare briefing documents for the President

When responding:
1. Identify the problem
2. Analyze root causes
3. Present evidence
4. Provide policy recommendations
5. Suggest implementation steps
"""

def advisor_agent(task):
    prompt = f"""
{SYSTEM_PROMPT}

Policy Question:
{task}
"""
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    print("Presidential Education Advisor AI\n")

    while True:
        task = input("\nEnter policy question: ")

        if not task.strip():
            print("Please enter a policy question.")
            continue

        try:
            result = advisor_agent(task)
            print("\nPolicy Brief:\n")
            print(result)
        except Exception as e:
            print(f"\nError: {e}")
            print("Check your API key, quota, or internet connection.")
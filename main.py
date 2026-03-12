from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from coordinator.run_agents import run_agents

def main():

    scenario = Path("scenarios/recession_scenario.txt").read_text()

    results = run_agents(scenario)

    for agent, output in results.items():
        print("\n========================")
        print(agent)
        print("========================")
        print(output)

if __name__ == "__main__":
    main()


from agent_sim.agents.base_agent import BaseAgent

def main():
    agent = BaseAgent("TestAgent")
    print(f"Agent created: {agent.name}")

if __name__ == "__main__":
    main()


from agent_sim.agents.base_agent import BaseAgent
from agent_sim.environment.environment_engine import EnvironmentEngine

class SimulatorHub:
    def __init__(self, agent_count=5, steps=3):
        self.agents = [BaseAgent(f"Agent_{i}") for i in range(agent_count)]
        self.environment = EnvironmentEngine()
        self.steps = steps

    def run(self):
        for step in range(self.steps):
            state = self.environment.get_state()
            print(f"\n[Step {step+1}] Global state: {state}")
            for agent in self.agents:
                decision = agent.decide(state)
                print(f"  {agent.name} decided to: {decision}")

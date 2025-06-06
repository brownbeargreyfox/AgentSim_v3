from agent_sim.world.environment import EnvironmentEngine
from agent_sim.agents.agent_registry import AgentRegistry

class SimulatorHub:
    def __init__(self, agents, steps=10):
        self.env = EnvironmentEngine()
        self.registry = AgentRegistry()
        for agent in agents:
            self.registry.register(agent)
        self.steps = steps

    def run(self):
        results = []
        for _ in range(self.steps):
            state = self.env.get_state()
            actions = self.registry.broadcast(state)
            results.append((state, actions))
        return results

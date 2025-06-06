class AgentRegistry:
    def __init__(self):
        self.agents = []

    def register(self, agent):
        self.agents.append(agent)

    def broadcast(self, state):
        return [agent.decide(state) for agent in self.agents]


class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.memory = []

    def decide(self, state):
        decision = "reflect" if state == "uncertain" else "act"
        self.memory.append((state, decision))
        return decision

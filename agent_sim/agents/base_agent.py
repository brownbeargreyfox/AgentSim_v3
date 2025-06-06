class BaseAgent:
    def __init__(self, name, decision_rules):
        self.name = name
        self.rules = decision_rules

    def decide(self, state):
        return self.rules.get(state, "observe")

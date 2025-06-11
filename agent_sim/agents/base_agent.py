class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.memory = []
        self.last_deterministic = None  # ✅ Needed for comparison in run_sim.py

    def decide(self, state):
        decision = "reflect" if state == "uncertain" else "act"
        self.last_deterministic = decision  # ✅ Track deterministic decision
        self.memory.append((state, decision))
        return decision

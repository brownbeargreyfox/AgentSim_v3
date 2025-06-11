class Agent:
    def __init__(self, name, goals, norms):
        self.name = name
        self.goals = goals
        self.norms = norms
        self.mood = 0.5
        self.override_history = {}
        self.memory = []  # Or load from memory_bank if you're using that

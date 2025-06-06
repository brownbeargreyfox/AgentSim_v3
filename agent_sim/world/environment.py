import random

class EnvironmentEngine:
    def __init__(self):
        self.seasons = ["calm", "conflict", "opportunity"]
        self.turn = 0

    def get_state(self):
        self.turn += 1
        return random.choice(self.seasons)


import random

class EnvironmentEngine:
    def get_state(self):
        return random.choice(["hungry", "tired", "uncertain", "bored"])

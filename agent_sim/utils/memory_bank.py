import json
import pandas as pd

class MemoryBank:
    # ... your existing init and methods ...

    def to_dataframe(self):
        return pd.DataFrame(
            self.history,
            columns=["State", "Decision", "Override?", "Result", "Utility"]
        )
        
class MemoryBank:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.history = []

    def add_memory(self, state, decision, override, result, utility):
        self.history.append((state, decision, override, result, utility))

    def save_to_disk(self, filepath=None):
        if filepath is None:
            filepath = f"{self.agent_name}_memory.json"
        with open(filepath, 'w') as f:
            json.dump(self.history, f, indent=2)

    def load_from_disk(self, filepath=None):
        if filepath is None:
            filepath = f"{self.agent_name}_memory.json"
        try:
            with open(filepath, 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

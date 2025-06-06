import json

class MemoryBank:
    def __init__(self):
        self.memories = []

    def add_memory(self, state, decision, overridden, result, utility):
        self.memories.append((state, decision, overridden, result, utility))

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.memories, f)

    def load(self, path):
        with open(path, 'r') as f:
            self.memories = json.load(f)

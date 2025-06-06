
import json

class MemoryBank:
    @staticmethod
    def save(agent, path):
        data = {
            "name": agent.name,
            "memory": agent.memory
        }
        with open(path, "w") as f:
            json.dump(data, f)

    @staticmethod
    def load(agent, path):
        with open(path, "r") as f:
            data = json.load(f)
            agent.name = data.get("name", agent.name)
            agent.memory = data.get("memory", [])

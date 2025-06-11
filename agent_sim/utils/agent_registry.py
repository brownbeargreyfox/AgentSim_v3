# In agent_sim/utils/agent_registry.py

from agent_sim.agents.agent import Agent
from typing import List, Optional, Dict

class AgentRegistry:
    """
    A class to manage all agents in the simulation, including registration,
    faction assignments, and lookup by name.
    """
    def __init__(self):
        self.agents: List[Agent] = []
        # --- ADD THIS to store factions ---
        self.agent_factions: Dict[str, Optional[str]] = {}

    def register(self, agent: Agent, faction: Optional[str] = None): # --- UPDATE the method signature ---
        """Adds an agent to the simulation registry and assigns its faction."""
        if agent not in self.agents:
            self.agents.append(agent)
            # --- ADD THIS line to save the faction ---
            self.agent_factions[agent.name] = faction

    def get_average_mood(self) -> float:
        """Calculates the average mood of the entire agent population."""
        if not self.agents:
            return 0.5
        return sum(agent.mood for agent in self.agents) / len(self.agents)

    def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """Finds and returns an agent from the registry by its unique name."""
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None
from agent_sim.agents.base_agent import BaseAgent
from agent_sim.simulator_hub import SimulatorHub

def main():
    agent1 = BaseAgent("Alpha", {"calm": "observe", "conflict": "fight", "opportunity": "explore"})
    agent2 = BaseAgent("Beta", {"calm": "meditate", "conflict": "negotiate", "opportunity": "innovate"})

    sim = SimulatorHub([agent1, agent2], steps=5)
    results = sim.run()
    for state, actions in results:
        print(f"State: {state} -> Actions: {actions}")

if __name__ == "__main__":
    main()

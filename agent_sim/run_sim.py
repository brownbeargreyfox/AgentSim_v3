
from agent_sim.simulator.simulator_hub import SimulatorHub

def main():
    sim = SimulatorHub(agent_count=10, steps=5)
    sim.run()

if __name__ == "__main__":
    main()

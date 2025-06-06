
from agent_sim.simulator.simulator_hub import SimulatorHub
from agent_sim.agents.base_agent import BaseAgent
from agent_sim.simulator.free_will_simulator import FreeWillSimulator
from agent_sim.environment.environment_engine import EnvironmentEngine
from agent_sim.utils.memory_bank import MemoryBank
import os

def main():
    env = EnvironmentEngine()
    agent = BaseAgent("Alice")

    # Load previous memory if available
    mem_file = "agent_alice_memory.json"
    if os.path.exists(mem_file):
        MemoryBank.load(agent, mem_file)
        print(f"Loaded memory for {agent.name}")

    fw_agent = FreeWillSimulator(agent, override_prob=0.5)

    for step in range(5):
        state = env.get_state()
        decision = fw_agent.decide(state)
        print(f"[Step {step+1}] State: {state} -> Decision: {decision}")

    # Save memory after run
    MemoryBank.save(agent, mem_file)
    print(f"Memory saved to {mem_file}")

if __name__ == "__main__":
    main()

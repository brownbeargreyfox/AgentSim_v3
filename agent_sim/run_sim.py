
import pandas as pd
from agent_sim.simulator.free_will_simulator import FreeWillSimulator
from agent_sim.agents.base_agent import BaseAgent
from agent_sim.environment.environment_engine import EnvironmentEngine
from agent_sim.utils.memory_bank import MemoryBank

def run_simulation_with_params(agent_name, override_prob, num_turns):
    agent = BaseAgent(agent_name)
    env = EnvironmentEngine()
    fw_agent = FreeWillSimulator(agent, override_prob=override_prob)

    results = []

    for i in range(num_turns):
        state = env.get_state()
        decision = fw_agent.decide(state)
        overridden = decision != agent.last_deterministic
        results.append({
            "Turn": i + 1,
            "State": state,
            "Deterministic": agent.last_deterministic,
            "Final Decision": decision,
            "Overridden": overridden
        })

    MemoryBank.save(agent, f"{agent_name.lower()}_memory.json")
    return pd.DataFrame(results)

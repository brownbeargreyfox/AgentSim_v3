
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

def run_multi_agent_sim(agent_params, num_turns=10):
    """
    agent_params: List of tuples like [(agent_name, override_prob), ...]
    """
    from agent_sim.environment.environment_engine import EnvironmentEngine
    from agent_sim.utils.memory_bank import MemoryBank
    from agent_sim.simulator.free_will_simulator import FreeWillSimulator
    from agent_sim.agents.base_agent import BaseAgent

    agents = []
    fw_wrappers = []
    for name, override_prob in agent_params:
        base = BaseAgent(name)
        fw = FreeWillSimulator(base, override_prob=override_prob)
        agents.append(base)
        fw_wrappers.append(fw)

    env = EnvironmentEngine()
    results = []

    for turn in range(num_turns):
        state = env.get_state()
        for i, fw_agent in enumerate(fw_wrappers):
            agent = agents[i]
            decision = fw_agent.decide(state)
            overridden = decision != agent.last_deterministic
            results.append({
                "Turn": turn + 1,
                "Agent": agent.name,
                "State": state,
                "Deterministic": agent.last_deterministic,
                "Final Decision": decision,
                "Overridden": overridden
            })
            MemoryBank.save(agent, f"{agent.name.lower()}_memory.json")

    return pd.DataFrame(results)


if __name__ == "__main__":
    agents = [("Alpha", 0.3), ("Beta", 0.7), ("Gamma", 0.5)]
    df = run_multi_agent_sim(agents, num_turns=15)
    print(df.head())

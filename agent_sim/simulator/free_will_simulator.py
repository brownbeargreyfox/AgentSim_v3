
import random

class FreeWillSimulator:
    def __init__(self, agent, override_prob=0.3):
        self.agent = agent
        self.override_prob = override_prob
        self.alt_actions = {
            "reflect": ["act", "wait", "observe"],
            "act": ["reflect", "improvise", "ask_for_help"]
        }

    def decide(self, state):
        det_decision = self.agent.decide(state)
        if random.random() < self.override_prob:
            override = random.choice(self.alt_actions.get(det_decision, ["do_nothing"]))
            self.agent.memory.append((state, det_decision, True, override))
            return override
        else:
            self.agent.memory.append((state, det_decision, False, det_decision))
            return det_decision

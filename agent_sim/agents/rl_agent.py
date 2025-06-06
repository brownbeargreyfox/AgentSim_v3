import random

class RLAgent:
    def __init__(self, name, states, actions):
        self.name = name
        self.q_table = {(s, a): 0.0 for s in states for a in actions}
        self.actions = actions
        self.epsilon = 0.1
        self.alpha = 0.5
        self.gamma = 0.9

    def decide(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        q_vals = {a: self.q_table[(state, a)] for a in self.actions}
        return max(q_vals, key=q_vals.get)

    def learn(self, state, action, reward, next_state):
        max_q = max(self.q_table[(next_state, a)] for a in self.actions)
        self.q_table[(state, action)] += self.alpha * (reward + self.gamma * max_q - self.q_table[(state, action)])

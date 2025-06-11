# In agent_sim/agents/agent.py
import json
import random
from typing import Dict, Any, List, Tuple, Optional

class Agent:
    """
    An advanced agent with a psychological profile that can now communicate
    its needs and intentions to other agents.
    """
    def __init__(self, name: str, goals: Dict[str, float], norms: Dict[str, float],
                 profile: Optional[Dict[str, float]] = None):
        self.name = name
        self.goals = goals
        self.norms = norms
        
        self.psychological_profile = {
            "optimism": 0.5, "curiosity": 0.5, "guilt": 0.5, "adaptability": 0.5,
            "gregariousness": 0.5, "trusting": 0.5, "spitefulness": 0.5, "forgiveness": 0.5,
            "industriousness": 0.5, "risk_aversion": 0.5, "patience": 0.5, "impulsiveness": 0.5,
            "resilience": 0.5, "volatility": 0.5, "deceitfulness": 0.5, "tenacity": 0.5, "creativity": 0.5
        }
        if profile:
            self.psychological_profile.update(profile)

        self.mood: float = 0.5
        self.mood_history: List[float] = [self.mood]
        
        self.inventory: Dict[str, int] = {'supplies': 10}
        self.trust_scores: Dict[str, float] = {}

        self.override_history: Dict[str, int] = {}
        self.action_history: Dict[str, int] = {}
        
        # --- NEW ATTRIBUTE for communication ---
        # Stores temporary utility modifiers based on messages received this turn.
        self.social_context: Dict[str, float] = {}

    # --- NEW METHOD: Speaking ---
    def generate_messages(self, registry) -> List[Dict]:
        """
        Based on needs and personality, generate a list of messages to send.
        """
        messages = []
        # Decide if we even want to talk, based on gregariousness
        if random.random() > self.psychological_profile['gregariousness']:
            return []

        # 1. Broadcast need if supplies are low
        if self.inventory['supplies'] < 5:
            messages.append({
                'recipient': 'ALL', # Broadcast to everyone
                'content': {'type': 'NEED', 'resource': 'supplies', 'level': self.inventory['supplies']}
            })

        # 2. Broadcast intent to high-trust agents
        # First, find the agent's likely action this turn
        # (This is a simplified lookahead, a real one would need the state)
        likely_action = max(self.goals, key=self.goals.get)

        if likely_action in ['share', 'help_others']:
            # Find trusted allies to signal cooperation
            allies = [name for name, trust in self.trust_scores.items() if trust > 0.7]
            for ally_name in allies:
                messages.append({
                    'recipient': ally_name,
                    'content': {'type': 'INTENT', 'action': 'cooperate'}
                })

        return messages

    # --- NEW METHOD: Listening ---
    def process_messages(self, received_messages: List[Dict]):
        """
        Processes incoming messages and updates internal social context for the turn.
        """
        print(f"[{self.name}] Processing {len(received_messages)} messages.")
        for msg in received_messages:
            sender = msg['sender']
            content = msg['message_content']
            msg_type = content.get('type')

            # An adaptable agent is more influenced by what it hears
            influence_factor = self.psychological_profile['adaptability']

            if msg_type == 'INTENT' and content.get('action') == 'cooperate':
                # A trusted agent intends to cooperate! This makes me want to cooperate too.
                trust_in_sender = self.trust_scores.get(sender, 0.5)
                cooperation_bonus = 0.2 * trust_in_sender * influence_factor
                
                # Temporarily boost the utility of cooperative actions for this turn
                self.social_context['share'] = self.social_context.get('share', 0.0) + cooperation_bonus
                self.social_context['help_others'] = self.social_context.get('help_others', 0.0) + cooperation_bonus

    def _evaluate_utility(self, decision: str, state: Dict[str, Any]) -> float:
        """Calculates utility, now also considering the social context from messages."""
        # (Previous logic for needs, goals, norms, and curiosity remains the same)
        need_for_supplies = 1.0 - (min(self.inventory['supplies'], 10) / 10)
        supply_gain = 0.0
        if decision == 'hoard': supply_gain = 0.8 * need_for_supplies
        elif decision == 'work': supply_gain = 0.4
        elif decision == 'share': supply_gain = -0.3
        
        goal_alignment = self.goals.get(decision, 0.0)
        norm_alignment = self.norms.get(decision, 0.0)
        
        times_chosen = self.action_history.get(decision, 0)
        curiosity_bonus = (1 / (1 + times_chosen)) * self.psychological_profile['curiosity'] * 0.2

        # --- UPDATED to use social context ---
        # Add any temporary utility bonus from messages received this turn.
        social_bonus = self.social_context.get(decision, 0.0)

        final_utility = (supply_gain * 0.5) + \
                        (goal_alignment * 0.25) + \
                        (norm_alignment * 0.15) + \
                        (curiosity_bonus * 0.05) + \
                        (social_bonus * 0.05) + \
                        (random.uniform(-0.05, 0.05))

        return final_utility

    def decide(self, state: Dict[str, Any], possible_decisions: List[str]) -> Tuple[str, bool]:
        """Decides on an action, after clearing previous turn's social context."""
        
        # --- NEW: Clear context at the start of every decision process ---
        self.social_context = {}

        # (The rest of the method is unchanged)
        if not possible_decisions:
            return "idle", False

        utilities = {d: self._evaluate_utility(d, state) for d in possible_decisions}
        logical_choice = max(utilities, key=utilities.get)

        override_chance = 0.8 * (1 - self.mood)
        will_override = random.random() < override_chance

        final_decision = logical_choice
        was_overridden = False
        if will_override and len(possible_decisions) > 1:
            choices = [d for d in possible_decisions if d != logical_choice]
            final_decision = random.choice(choices)
            was_overridden = True
            key = str((state.get('name'), logical_choice))
            self.override_history[key] = self.override_history.get(key, 0) + 1
            
        self.action_history[final_decision] = self.action_history.get(final_decision, 0) + 1

        return final_decision, was_overridden

    # (The learn, update_trust, save_profile, and load_profile methods are unchanged)
    def learn(self, state_name: str, decision: str, override: bool, result: str, utility: float):
        optimism_factor = self.psychological_profile['optimism']
        mood_change = (utility - 0.5) * 0.1
        if mood_change < 0:
            mood_change *= (1.5 - optimism_factor)
        if decision in ['hoard', 'ignore']:
            mood_change += self.psychological_profile['guilt'] * -0.05
        self.mood += mood_change
        self.mood = max(0.0, min(1.0, self.mood))
        self.mood_history.append(self.mood)

    def update_trust(self, other_agent_name: str, amount: float):
        current_trust = self.trust_scores.get(other_agent_name, 0.5)
        new_trust = current_trust + amount
        self.trust_scores[other_agent_name] = max(0.0, min(1.0, new_trust))
        print(f"[{self.name}] Trust in {other_agent_name} updated to {self.trust_scores[other_agent_name]:.2f}")

    def save_profile(self, filepath: str = None):
        if filepath is None:
            filepath = f"{self.name}_profile.json"
        profile_data = {
            "name": self.name, "mood": self.mood, "goals": self.goals, "norms": self.norms,
            "inventory": self.inventory, "trust_scores": self.trust_scores,
            "override_history": self.override_history, "action_history": self.action_history,
            "psychological_profile": self.psychological_profile
        }
        with open(filepath, 'w') as f:
            json.dump(profile_data, f, indent=4)
        print(f"[{self.name}] Full profile saved to {filepath}")

    @classmethod
    def load_profile(cls, filepath: str):
        with open(filepath, 'r') as f:
            data = json.load(f)
        agent = cls(name=data['name'], goals=data['goals'], norms=data['norms'],
                    profile=data.get('psychological_profile'))
        agent.mood = data.get('mood', 0.5)
        agent.inventory = data.get('inventory', {'supplies': 10})
        agent.trust_scores = data.get('trust_scores', {})
        agent.override_history = data.get('override_history', {})
        agent.action_history = data.get('action_history', {})
        agent.mood_history.append(agent.mood)
        print(f"[{agent.name}] Full profile loaded from {filepath}")
        return agent
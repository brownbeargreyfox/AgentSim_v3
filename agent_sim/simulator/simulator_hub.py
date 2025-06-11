# In agent_sim/simulator/simulator_hub.py
import random
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import pandas as pd
from collections import Counter

# Correctly placed imports
from agent_sim.utils.agent_registry import AgentRegistry
from agent_sim.agents.agent import Agent


# --- This is the new class for communication ---
class DialogueManager:
    """
    Manages the queuing and distribution of symbolic messages between agents
    during a single simulation step.
    """
    def __init__(self):
        self.message_queue = []

    def queue_message(self, sender: str, recipient: str, message: dict):
        """Adds a message to the queue for this turn."""
        self.message_queue.append({
            "sender": sender,
            "recipient": recipient,
            "message_content": message
        })

    def get_messages_for_agent(self, agent_name: str) -> list:
        """Returns all messages addressed to a specific agent."""
        return [msg for msg in self.message_queue if msg['recipient'] == agent_name]

    def clear_queue(self):
        """Wipes the message queue. Called at the end of a turn."""
        self.message_queue = []


# --- This is the single, correct SimulatorHub class ---
class SimulatorHub:
    def __init__(self, env, registry: AgentRegistry):
        self.env = env
        self.registry = registry
        self.time_step = 0
        
        # Enhanced logging for new dynamics
        self.interactions = []
        self.conflicts = []
        self.decision_log = []
        self.wealth_log = []
        
        # The dialogue manager is initialized here
        self.dialogue_manager = DialogueManager()

    def _run_communication_phase(self):
        """
        Runs the new communication phase where agents can "speak" and "listen"
        before making decisions.
        """
        print("...Running Communication Phase...")
        self.dialogue_manager.clear_queue()

        # 1. Agents generate messages based on their state
        for agent in self.registry.agents:
            # We will add the generate_messages method to the Agent class next
            messages = agent.generate_messages(self.registry)
            for msg in messages:
                self.dialogue_manager.queue_message(
                    sender=agent.name,
                    recipient=msg['recipient'],
                    message=msg['content']
                )

        # 2. Agents process the messages they've received
        for agent in self.registry.agents:
            received_messages = self.dialogue_manager.get_messages_for_agent(agent.name)
            if received_messages:
                # We will add the process_messages method to the Agent class next
                agent.process_messages(received_messages)

    def run_simulation_step(self):
        """
        Runs a single, multi-phase step of the simulation, now starting with communication.
        """
        self.time_step += 1
        state = self.env.get_state()
        print(f"\n--- TIME STEP {self.time_step} | {state['name']} | World Supplies: {state['resources']} ---")

        # --- PHASE 1: COMMUNICATION (NEW) ---
        # The new communication phase is called at the start of each turn.
        self._run_communication_phase()

        # --- PHASE 2: AGENT DECISION-MAKING ---
        decisions = {}
        for agent in self.registry.agents:
            decision, was_override = agent.decide(state, state['decisions'])
            decisions[agent.name] = {'action': decision, 'overridden': was_override}
            print(f"[{agent.name}] Decides to '{decision}'. Mood: {agent.mood:.2f}, Supplies: {agent.inventory['supplies']}")
            
        # --- PHASE 3: APPLY CONSEQUENCES & MANAGE RESOURCES ---
        self._apply_resource_consequences(decisions)

        # --- PHASE 4: UPDATE SOCIAL DYNAMICS & TRUST ---
        self._update_social_dynamics(decisions)
        
        # --- PHASE 5: AGENT LEARNING & MOOD UPDATE ---
        for agent in self.registry.agents:
            agent_decision = decisions[agent.name]['action']
            was_override = decisions[agent.name]['overridden']
            
            utility = agent._evaluate_utility(agent_decision, state)
            result = f"Action '{agent_decision}' yielded subjective utility {utility:.2f}"
            
            agent.learn(state['name'], agent_decision, was_override, result, utility)
            self.decision_log.append((agent.name, agent_decision))
        
        # --- PHASE 6: GLOBAL UPDATES ---
        self._apply_emotional_contagion()
        self.wealth_log.append(sum(a.inventory['supplies'] for a in self.registry.agents))

    def _apply_resource_consequences(self, decisions: dict):
        """Processes how each decision affects agent and world resources."""
        print("...Applying resource consequences...")
        for name, decision_data in decisions.items():
            agent = self.registry.get_agent_by_name(name)
            action = decision_data['action']

            if action == 'work':
                if self.env.world_resources > 0:
                    agent.inventory['supplies'] += 1
                    self.env.update_resources(-1)
            elif action == 'innovate':
                if agent.inventory['supplies'] >= 3:
                    agent.inventory['supplies'] -= 3

    def _update_social_dynamics(self, decisions: dict):
        """Processes interactions between agents, updating trust and logging events."""
        print("...Updating social dynamics and trust...")
        agent_names = list(decisions.keys())
        cooperative_actions = {'share', 'help_others'}
        selfish_actions = {'hoard', 'ignore'}

        for i in range(len(agent_names)):
            for j in range(i + 1, len(agent_names)):
                name1, name2 = agent_names[i], agent_names[j]
                agent1 = self.registry.get_agent_by_name(name1)
                agent2 = self.registry.get_agent_by_name(name2)
                
                action1 = decisions[name1]['action']
                action2 = decisions[name2]['action']

                if action1 in cooperative_actions and action2 in cooperative_actions:
                    agent1.update_trust(name2, 0.1)
                    agent2.update_trust(name1, 0.1)
                    self.interactions.append((name1, name2, {'event': 'Cooperation', 'weight': 0.8}))
                    if agent1.inventory['supplies'] > 0:
                        agent1.inventory['supplies'] -= 1
                        agent2.inventory['supplies'] += 1
                
                elif action1 in cooperative_actions and action2 in selfish_actions:
                    agent1.update_trust(name2, -0.2)
                    agent2.update_trust(name1, 0.05)
                    self.conflicts.append((name1, name2, self.time_step))
                    self.interactions.append((name1, name2, {'event': 'Betrayal', 'weight': 0.2}))

                elif action2 in cooperative_actions and action1 in selfish_actions:
                    agent2.update_trust(name1, -0.2)
                    agent1.update_trust(name2, 0.05)
                    self.conflicts.append((name1, name2, self.time_step))
                    self.interactions.append((name1, name2, {'event': 'Betrayal', 'weight': 0.2}))

    def _apply_emotional_contagion(self):
        """Nudges agent moods toward the population average."""
        if len(self.registry.agents) < 2:
            return
        avg_mood = self.registry.get_average_mood()
        for agent in self.registry.agents:
            agent.mood = (agent.mood * 0.95) + (avg_mood * 0.05)

    # --- VISUALIZATION METHODS ---
    # (No changes needed to any of the visualization methods)
    def visualize_trust_network(self):
        G = nx.DiGraph()
        for agent in self.registry.agents:
            for target_agent, trust_score in agent.trust_scores.items():
                G.add_edge(agent.name, target_agent, weight=trust_score)
        if not G.edges():
            print("No trust relationships to visualize.")
            return
        edge_widths = [d['weight'] * 4 for _, _, d in G.edges(data=True)]
        edge_colors = [d['weight'] for _, _, d in G.edges(data=True)]
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=0.8)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12,
                width=edge_widths, edge_cmap=plt.cm.Greens, edge_color=edge_colors, arrows=True)
        plt.title("Agent Trust Network")
        plt.show()

    def visualize_wealth_distribution(self):
        wealth_data = [agent.inventory['supplies'] for agent in self.registry.agents]
        plt.figure(figsize=(10, 5))
        sns.histplot(wealth_data, bins=10, kde=True)
        plt.title("Agent Wealth Distribution")
        plt.xlabel("Number of Supplies")
        plt.ylabel("Number of Agents")
        plt.show()

    def visualize_mood_trajectories(self):
        mood_log = {agent.name: agent.mood_history for agent in self.registry.agents}
        if not mood_log:
            print("No mood history found.")
            return
        df = pd.DataFrame(mood_log)
        df.plot(figsize=(12, 6), title="Agent Mood Trajectories Over Time")
        plt.xlabel("Time Step")
        plt.ylabel("Mood")
        plt.grid(True)
        plt.show()
# In agent_sim/environment/environment_engine.py
import random

class EnvironmentEngine:
    def __init__(self, settings: dict):
        """Initializes the environment based on scenario settings."""
        self.world_resources = settings.get("initial_resources", 100)
        self.states = settings.get("state_sequence", ["Festival"])
        self.crisis_events = settings.get("crisis_events", [])
        self.step = 0
        print("EnvironmentEngine initialized from scenario settings.")

    def get_state(self):
        """Gets the current state and checks for crisis events."""
        # Get the base state by cycling through the sequence
        state_template = self.states[self.step % len(self.states)]
        current_state = {"name": state_template} # Start with just the name
        
        # Check if a crisis event is triggered on this turn
        for event in self.crisis_events:
            if event.get("trigger_turn") == self.step:
                print(f"CRISIS EVENT TRIGGERED: {event['name']}")
                # Pass the crisis effect data into the state
                current_state['crisis'] = event['effect']
        
        # Add resource and decision info to the state
        # In a more advanced version, decisions could also come from the state_template
        current_state['resources'] = self.world_resources
        current_state['decisions'] = ["hoard", "share", "innovate", "work", "celebrate", "help_others", "ignore"]

        self.step += 1
        return current_state

    def update_resources(self, amount_changed: int):
        """Updates the world's resource pool."""
        self.world_resources += amount_changed
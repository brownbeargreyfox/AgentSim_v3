# In agent_sim/utils/scenario_loader.py
import json

def load_scenario(filepath: str) -> dict:
    """Loads a simulation scenario from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            scenario_data = json.load(f)
        print(f"Successfully loaded scenario: {scenario_data.get('scenario_name', 'Unnamed Scenario')}")
        # Add validation here in the future if needed
        return scenario_data
    except FileNotFoundError:
        print(f"Error: Scenario file not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in scenario file: {filepath}")
        return None
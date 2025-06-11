import streamlit as st
import pandas as pd
import json
import sys
import io

# --- Core Simulation Components (using absolute imports) ---
from agent_sim.agents.agent import Agent
from agent_sim.utils.agent_registry import AgentRegistry
from agent_sim.environment.environment_engine import EnvironmentEngine
from agent_sim.simulator.simulator_hub import SimulatorHub
from agent_sim.utils.scenario_loader import load_scenario

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="AgentSim Scenario Runner")

# --- Helper Functions ---

def initialize_simulation_from_scenario(scenario_data):
    """Creates simulation objects based on a loaded scenario dictionary."""
    st.session_state.log = [f"--- Loading Scenario: {scenario_data.get('scenario_name')} ---"]
    
    env_settings = scenario_data.get("environment_settings", {})
    archetypes = scenario_data.get("agent_archetypes", {})
    population = scenario_data.get("population_setup", [])

    env = EnvironmentEngine(settings=env_settings)
    registry = AgentRegistry()

    for pop_group in population:
        archetype_name = pop_group.get("archetype")
        archetype_data = archetypes.get(archetype_name)
        if not archetype_data:
            st.error(f"Archetype '{archetype_name}' not found in scenario file!")
            continue
        
        for i in range(pop_group.get("count", 0)):
            agent_name = f"{archetype_name}-{i+1}"
            
            # --- THIS IS THE KEY UPDATE ---
            # We now create the agent with its psychological profile from the scenario.
            agent = Agent(
                name=agent_name,
                goals=archetype_data.get("goals", {}),
                norms=archetype_data.get("norms", {}),
                profile=archetype_data.get("psychological_profile") # Pass the new profile
            )
            
            agent.inventory = archetype_data.get("initial_inventory", {'supplies': 10})
            registry.register(agent, faction=pop_group.get("faction"))

    st.session_state.hub = SimulatorHub(env, registry)
    st.success(f"Scenario '{scenario_data.get('scenario_name')}' initialized!")


def capture_and_log_output(func_to_run):
    """Captures print output from a function and adds it to the log."""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    func_to_run() # Run the function (e.g., hub.run_simulation_step)
    
    output = captured_output.getvalue()
    sys.stdout = old_stdout # Restore stdout
    
    if output:
        st.session_state.log.extend(output.strip().split('\n'))


# --- Initialize Session State ---
if 'hub' not in st.session_state:
    st.session_state.hub = None
if 'log' not in st.session_state:
    st.session_state.log = ["Welcome! Please load a scenario to begin."]

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("?? Scenario Control")
    uploaded_file = st.file_uploader("Upload a Scenario File", type=["json"])
    
    if uploaded_file is not None:
        try:
            scenario_data = json.load(uploaded_file)
            if st.button("?? Initialize From Scenario"):
                initialize_simulation_from_scenario(scenario_data)
        except Exception as e:
            st.error(f"Failed to read or parse scenario file: {e}")

    # Show run controls only after initialization
    if st.session_state.hub:
        st.divider()
        st.header("?? Simulation Controls")
        if st.button("?? Run One Step"):
            capture_and_log_output(st.session_state.hub.run_simulation_step)

        num_steps_input = st.number_input("Run multiple steps:", min_value=1, max_value=100, value=10)
        if st.button(f"? Run {num_steps_input} Steps"):
            with st.spinner(f"Running {num_steps_input} steps..."):
                for _ in range(num_steps_input):
                    capture_and_log_output(st.session_state.hub.run_simulation_step)
            st.success("Run complete.")

# --- Main Dashboard Area ---
st.title("AgentSim Scenario Dashboard")

if not st.session_state.hub:
    st.info("Upload and initialize a scenario from the sidebar to begin.")
else:
    hub = st.session_state.hub
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Time Step", hub.time_step)
    col2.metric("Agent Count", len(hub.registry.agents))
    col3.metric("Average Mood", f"{hub.registry.get_average_mood():.2f}")
    col4.metric("World Supplies", hub.env.world_resources)
    st.divider()

    main_col1, main_col2 = st.columns([2, 1.5])

   # In interface/gui_control.py

    with main_col1:
        st.subheader("?? Agent Status")
        
        # Create a live DataFrame of agent data
        agent_data = []
        for agent in hub.registry.agents:
            avg_trust = (sum(agent.trust_scores.values()) / len(agent.trust_scores)) if agent.trust_scores else 0.5
            agent_data.append({
                "Name": agent.name, # This line was likely missing or had a typo.
                "Mood": agent.mood,
                "Supplies": agent.inventory.get('supplies', 0),
                "Optimism": agent.psychological_profile.get('optimism', 0.5),
                "Avg. Trust": avg_trust
            })
        
        df_agents = pd.DataFrame(agent_data)

        # --- NEW: Add a check to prevent the error if no agents exist ---
        if not df_agents.empty:
            df_agents = df_agents.set_index("Name")
            st.dataframe(df_agents.style.format({
                "Mood": "{:.2f}",
                "Avg. Trust": "{:.2f}",
                "Optimism": "{:.2f}"
            }).background_gradient(cmap='RdYlGn', subset=['Mood'])
              .background_gradient(cmap='Blues', subset=['Supplies'])
              .background_gradient(cmap='Greens', subset=['Optimism']),
              use_container_width=True)
        else:
            st.warning("No agent data to display yet.")


        st.subheader("?? Mood Trajectories")
        mood_history = {agent.name: agent.mood_history for agent in hub.registry.agents}
        # Add another check for robustness
        if mood_history:
            df_mood = pd.DataFrame(mood_history)
            st.line_chart(df_mood)
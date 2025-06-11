import streamlit as st
import json
import copy

# --- Default Template for a New Scenario ---
# This provides a starting point when the editor is opened.
DEFAULT_SCENARIO_TEMPLATE = {
  "scenario_name": "New Scenario",
  "environment_settings": {
    "initial_resources": 100,
    "state_sequence": ["Festival", "Resource Scarcity", "Storm"],
    "crisis_events": []
  },
  "agent_archetypes": {
    "default_agent": {
      "goals": {"work": 0.5, "share": 0.5},
      "norms": {"help_others": 0.5, "hoard": -0.5},
      "initial_inventory": {"supplies": 10}
    }
  },
  "population_setup": [
    {
      "archetype": "default_agent",
      "count": 10,
      "faction": "Unaffiliated"
    }
  ]
}

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="AgentSim Scenario Editor")

# --- Initialize Session State ---
# This is crucial for keeping your edits live without resetting the page.
if 'scenario' not in st.session_state:
    # Use deepcopy to ensure the template isn't modified by user edits
    st.session_state.scenario = copy.deepcopy(DEFAULT_SCENARIO_TEMPLATE)

st.title("📝 AgentSim Scenario Editor")
st.caption("Design your simulation experiments here. Load, edit, and save scenario files.")
st.divider()

# --- Main Editor Layout (2 columns) ---
editor_col, controls_col = st.columns([2, 1])

# --- COLUMN 1: The Scenario Editor ---
with editor_col:
    st.header("Scenario Details")

    # Edit basic scenario info
    st.session_state.scenario['scenario_name'] = st.text_input(
        "Scenario Name",
        value=st.session_state.scenario.get('scenario_name', 'New Scenario')
    )

    # --- Environment Editor ---
    with st.expander("🌍 Environment Settings", expanded=True):
        env_settings = st.session_state.scenario.get('environment_settings', {})
        env_settings['initial_resources'] = st.slider(
            "Initial World Resources", 0, 500, env_settings.get('initial_resources', 100)
        )
        # For simplicity, we'll use a text area for the state sequence
        state_sequence_str = "\n".join(env_settings.get('state_sequence', []))
        new_sequence_str = st.text_area(
            "State Sequence (one state per line)",
            value=state_sequence_str,
            height=100
        )
        env_settings['state_sequence'] = [line.strip() for line in new_sequence_str.split('\n') if line.strip()]

    # --- Archetype Editor ---
    with st.expander("🧑‍🔬 Agent Archetype Editor", expanded=True):
        archetypes = st.session_state.scenario.get('agent_archetypes', {})
        
        if not archetypes:
            st.warning("No archetypes defined!")
        else:
            selected_archetype = st.selectbox("Select Archetype to Edit", options=list(archetypes.keys()))
            
            if selected_archetype:
                st.write(f"**Editing: `{selected_archetype}`**")
                arch_data = archetypes[selected_archetype]
                
                # Use st.json_editor for a powerful, flexible way to edit goals and norms
                arch_data['goals'] = st.data_editor(arch_data.get('goals', {}), key=f"{selected_archetype}_goals")
                arch_data['norms'] = st.data_editor(arch_data.get('norms', {}), key=f"{selected_archetype}_norms")
                
                inv_settings = arch_data.get('initial_inventory', {})
                inv_settings['supplies'] = st.number_input(
                    "Initial Supplies", value=inv_settings.get('supplies', 10), key=f"{selected_archetype}_supplies"
                )

        # Add a new archetype
        new_archetype_name = st.text_input("New Archetype Name", key="new_arch_name")
        if st.button("Add New Archetype") and new_archetype_name:
            if new_archetype_name in archetypes:
                st.error("Archetype with this name already exists.")
            else:
                archetypes[new_archetype_name] = {
                    "goals": {"work": 0.5}, "norms": {}, "initial_inventory": {"supplies": 10}
                }
                st.rerun()

    # --- Population Editor ---
    with st.expander("👨‍👩‍👧‍👦 Population Setup", expanded=True):
        population = st.session_state.scenario.get('population_setup', [])
        for i, pop_group in enumerate(population):
            st.write(f"--- Group {i+1} ---")
            cols = st.columns(3)
            pop_group['archetype'] = cols[0].selectbox(
                "Archetype", options=list(archetypes.keys()), index=list(archetypes.keys()).index(pop_group['archetype']), key=f"pop_{i}_arch"
            )
            pop_group['count'] = cols[1].number_input("Count", min_value=1, value=pop_group['count'], key=f"pop_{i}_count")
            pop_group['faction'] = cols[2].text_input("Faction", value=pop_group.get('faction', 'None'), key=f"pop_{i}_faction")


# --- COLUMN 2: File Controls and Raw JSON View ---
with controls_col:
    st.header("Controls & Actions")
    
    # --- File Operations ---
    st.subheader("💾 File Operations")
    
    # Load a scenario from a file
    uploaded_file = st.file_uploader("Load Scenario from JSON", type=["json"])
    if uploaded_file is not None:
        try:
            # When a file is uploaded, replace the current scenario in the session state
            st.session_state.scenario = json.load(uploaded_file)
            st.success("Scenario loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    # Save the current scenario to a file
    st.download_button(
        label="📥 Save Current Scenario",
        data=json.dumps(st.session_state.scenario, indent=2),
        file_name=f"{st.session_state.scenario.get('scenario_name', 'scenario').replace(' ', '_')}.json",
        mime="application/json"
    )

    st.divider()

    # --- Raw JSON Preview ---
    st.subheader("📄 Live Scenario JSON")
    st.json(st.session_state.scenario)
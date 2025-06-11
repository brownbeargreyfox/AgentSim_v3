import streamlit as st
import json
import random

# --- PRESET DEFINITIONS ---
# This is where the "creative" logic lives. You can easily add more presets here.

WORLD_PRESETS = {
    "Lush Paradise": {
        "description": "A world of abundance and calm. Resources are plentiful, and crises are rare.",
        "initial_resources": 500,
        "state_sequence": ["Festival", "Festival", "Period of Peace", "Build", "Unexpected Boon"],
        "crisis_chance": 0.05 # 5% chance of a minor crisis
    },
    "Harsh Tundra": {
        "description": "A brutal, unforgiving landscape. Resources are scarce and survival is a daily struggle.",
        "initial_resources": 40,
        "state_sequence": ["Resource Scarcity", "Storm", "Resource Scarcity", "Cold", "Resource Scarcity"],
        "crisis_chance": 0.3 # 30% chance of a crisis
    },
    "Post-Apocalyptic Ruin": {
        "description": "A shattered world after a great collapse. Pockets of resources exist, but so do unknown dangers and conflict.",
        "initial_resources": 60,
        "state_sequence": ["Resource Scarcity", "Ruins", "Conflict", "Sudden Storm", "Ruins"],
        "crisis_chance": 0.5 # 50% chance of a crisis
    },
    "Magical Anarchy": {
        "description": "A chaotic world where amazing boons and terrible curses appear at random. Highly unpredictable.",
        "initial_resources": 150,
        "state_sequence": ["Unexpected Boon", "Curse", "Festival", "Conflict", "Strange Phenomenon"],
        "crisis_chance": 0.75 # 75% chance of something wild happening
    },
    "Techno-Utopia": {
        "description": "A highly advanced society where resources are generated, but social and political conflict is common.",
        "initial_resources": 300,
        "state_sequence": ["Build", "Innovate", "Political Unrest", "Innovate", "Festival"],
        "crisis_chance": 0.2
    }
}

SOCIETY_PRESETS = {
    "Cooperative Harmony": {
        "description": "A society composed of helpers, builders, and diplomats.",
        "archetype_palette": ["stalwart_settler", "the_mediator", "charming_diplomat", "the_disciple", "settler_young_idealist"]
    },
    "Waring Tribes": {
        "description": "A volatile mix of aggressive, spiteful, and zealous agents.",
        "archetype_palette": ["raider", "antagonist_thug", "the_zealot", "the_traditionalist", "grudge_holding_merchant"]
    },
    "Suspicious Survivors": {
        "description": "A population of paranoid, risk-averse agents just trying to make it through the day.",
        "archetype_palette": ["resilient_survivor", "paranoid_hoarder", "hermit_fearful_recluse", "cautious_planner", "settler_grizzled_veteran"]
    },
    "Chaotic Innovators": {
        "description": "A society of brilliant but unstable geniuses, artists, and tricksters.",
        "archetype_palette": ["impulsive_innovator", "unstable_genius", "the_trickster", "spirited_artist", "the_gambler"]
    },
    "Aspiring Meritocracy": {
        "description": "A competitive mix of investors, planners, and hard-working innovators.",
        "archetype_palette": ["the_shrewd_investor", "innovator_focused_genius", "cautious_planner", "the_bureaucrat", "survivor_community_leader"]
    }
}

CRISIS_EVENTS_POOL = [
    {"name": "Blight", "effect": {"type": "destroy_supplies_percent", "value": 0.4}},
    {"name": "Economic Crash", "effect": {"type": "destroy_supplies_percent", "value": 0.6}},
    {"name": "Sudden Famine", "effect": {"type": "destroy_supplies_percent", "value": 0.8}},
    {"name": "Social Unrest", "effect": {"type": "trust_degradation", "value": -0.2}} # A potential future effect
]

# --- Main Generator Function ---
def generate_scenario(world_key, society_key, population_size, chaos_factor, turn_count):
    world_preset = WORLD_PRESETS[world_key]
    society_preset = SOCIETY_PRESETS[society_key]
    
    # 1. Generate Environment Settings
    env_settings = {
        "initial_resources": world_preset["initial_resources"],
        "state_sequence": world_preset["state_sequence"],
        "crisis_events": []
    }
    # Add crisis events based on chaos factor
    for turn in range(1, turn_count):
        if random.random() < world_preset["crisis_chance"] * chaos_factor:
            crisis = random.choice(CRISIS_EVENTS_POOL).copy()
            crisis["trigger_turn"] = turn
            env_settings["crisis_events"].append(crisis)

    # 2. Generate Population Setup
    population_setup = []
    archetype_palette = society_preset["archetype_palette"]
    
    # Simple distribution: give each archetype in the palette a rough share of the population
    num_archetypes = len(archetype_palette)
    base_count = population_size // num_archetypes
    remainder = population_size % num_archetypes
    
    for i, archetype in enumerate(archetype_palette):
        count = base_count + (1 if i < remainder else 0)
        if count > 0:
            population_setup.append({
                "archetype": archetype,
                "count": count,
                "faction": f"{archetype.split('_')[-1].capitalize()} Faction"
            })

    # 3. Assemble the final scenario object
    final_scenario = {
        "scenario_name": f"{population_size} {society_key} in a {world_key}",
        "environment_settings": env_settings,
        "agent_archetypes": {}, # This will be filled from your master file
        "population_setup": population_setup
    }
    
    return final_scenario

# --- Streamlit GUI ---
st.set_page_config(layout="centered", page_title="The World Forge")
st.title("🌍 The World Forge")
st.caption("Generate complex simulation scenarios from high-level concepts.")

with st.container(border=True):
    st.header("1. Choose Your Canvas")
    world_choice = st.selectbox("Select a World Theme:", options=list(WORLD_PRESETS.keys()))
    st.write(f"_{WORLD_PRESETS[world_choice]['description']}_")
    
    society_choice = st.selectbox("Select a Societal Archetype:", options=list(SOCIETY_PRESETS.keys()))
    st.write(f"_{SOCIETY_PRESETS[society_choice]['description']}_")

with st.container(border=True):
    st.header("2. Set the Scale & Intensity")
    population_slider = st.slider("Total Population Size:", min_value=10, max_value=500, value=100, step=5)
    turn_slider = st.slider("Number of Simulation Turns:", min_value=10, max_value=200, value=50, step=10)
    chaos_slider = st.select_slider(
        "Chaos & Crisis Factor:",
        options=["Low (Stable)", "Medium (Unpredictable)", "High (Chaotic)"],
        value="Medium (Unpredictable)"
    )
    chaos_map = {"Low (Stable)": 0.5, "Medium (Unpredictable)": 1.0, "High (Chaotic)": 1.5}
    chaos_value = chaos_map[chaos_slider]

if st.button("🔥 Forge World Scenario", type="primary", use_container_width=True):
    # Generate the scenario
    generated_scenario = generate_scenario(world_choice, society_choice, population_slider, chaos_value, turn_slider)
    st.session_state.generated_scenario = generated_scenario
    st.success("Scenario Forged Successfully!")

if 'generated_scenario' in st.session_state:
    st.divider()
    st.header("3. Your Generated Scenario")
    
    scenario_json = json.dumps(st.session_state.generated_scenario, indent=2)
    st.json(scenario_json)
    
    st.download_button(
        label="📥 Download Scenario File",
        data=scenario_json,
        file_name=f"{st.session_state.generated_scenario['scenario_name'].replace(' ', '_').lower()}.json",
        mime="application/json",
        use_container_width=True
    )
    st.info("NOTE: This generator only creates the scenario structure. You still need to paste your full 'agent_archetypes' library into the downloaded file before running it in the simulation GUI.")
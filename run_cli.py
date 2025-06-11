# gui.py
import streamlit as st
from agent_sim.environment.environment_engine import EnvironmentEngine
from agent_sim.agents.base_agent import BaseAgent
from agent_sim.simulator.simulator_hub import SimulatorHub
from agent_sim.utils.agent_registry import AgentRegistry

st.set_page_config(layout="wide")
st.title("AgentSim v3 - GUI Dashboard")

if 'hub' not in st.session_state:
    st.session_state.hub = None

num_agents = st.sidebar.slider("Number of Agents", 1, 100, 10)
num_turns = st.sidebar.number_input("Number of Turns", 1, 10000, 100)

if st.sidebar.button("🚀 Start Simulation"):
    env = EnvironmentEngine()
    registry = AgentRegistry()
    for i in range(num_agents):
        agent = BaseAgent(name=f"Agent-{i+1}")
        registry.register(agent)
    hub = SimulatorHub(env, registry)
    for _ in range(num_turns):
        hub.run_simulation_step()
    st.session_state.hub = hub
    st.success("Simulation complete.")

if st.session_state.hub:
    hub = st.session_state.hub
    st.metric("Current Step", hub.time_step)
    st.metric("Average Mood", f"{hub.registry.get_average_mood():.2f}")

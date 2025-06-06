import streamlit as st

st.title("AgentSim GUI")

st.sidebar.header("Simulation Controls")
agents = st.sidebar.slider("Number of agents", 1, 100, 10)
steps = st.sidebar.slider("Simulation steps", 1, 200, 50)

if st.button("Run Simulation"):
    st.write(f"Running with {agents} agents for {steps} steps...")

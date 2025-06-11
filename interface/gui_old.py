
import streamlit as st
import pandas as pd
import os
import json
from agent_sim.run_sim import run_multi_agent_sim
from agent_sim.run_sim import run_simulation_with_params

st.set_page_config(page_title="AgentSim Interactive GUI", layout="centered")
st.title("🧠 AgentSim GUI Control Panel")

st.markdown("Configure and run your simulation:")

# Sidebar agent settings
st.sidebar.header("Agent Settings")
agent_name = st.sidebar.text_input("Agent Name", value="Alice")
override_prob = st.sidebar.slider("Override Probability", 0.0, 1.0, 0.5, 0.05)
num_turns = st.sidebar.slider("Number of Turns", 1, 5000, 50, 500)

# Run simulation button
if st.button("Run Simulation"):
    st.write(f"Running simulation for {agent_name} with override probability {override_prob} for {num_turns} turns...")
    results_df = run_simulation_with_params(agent_name, override_prob, num_turns)

    if results_df is not None:
        st.success("Simulation complete!")
        st.dataframe(results_df)

        st.markdown("### Decision Statistics")
        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(results_df["Final Decision"].value_counts())

        with col2:
            st.line_chart(results_df["Overridden"].astype(int).cumsum())

        mem_file = f"{agent_name.lower()}_memory.json"
        st.download_button("Download Memory JSON", json.dumps(results_df.to_dict()), file_name=mem_file)

else:
    st.info("Configure parameters and click Run Simulation to begin.")


if st.button("Run Multi-Agent Simulation"):
    multi_agent_list = [("Alice", 0.2), ("Bob", 0.5), ("Char", 0.8)]
    df = run_multi_agent_sim(multi_agent_list, num_turns)
    st.dataframe(df)
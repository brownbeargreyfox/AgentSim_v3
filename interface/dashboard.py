
import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="AgentSim Dashboard", layout="wide")

st.title("🧠 AgentSim Free Will Simulator Dashboard")

memory_path = "agent_alice_memory.json"

if not os.path.exists(memory_path):
    st.warning(f"No memory file found at {memory_path}. Run the simulation first.")
else:
    with open(memory_path, "r") as f:
        agent_data = json.load(f)

    st.subheader(f"Agent: {agent_data['name']}")
    st.markdown(f"### Mood: `{agent_data.get('mood', 'N/A')}`")

    memory = agent_data.get("memory", [])
    if memory:
        df = pd.DataFrame(memory, columns=["State", "Deterministic", "Overridden", "Final Decision", "Utility"])
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📊 Decision Metrics")
        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(df["State"].value_counts(), use_container_width=True)

        with col2:
            st.bar_chart(df["Final Decision"].value_counts(), use_container_width=True)

        st.markdown("### 📈 Override Trend")
        df["Step"] = range(1, len(df) + 1)
        df["Override Numeric"] = df["Overridden"].astype(int)
        st.line_chart(df.set_index("Step")["Override Numeric"])
    else:
        st.info("Memory is empty.")


# AgentSim v3

**A Scalable, Modular Agent-Based Free Will Simulation**

## 🧠 Features

- Deterministic, Free Will, and RL Agent classes
- Environment engine with dynamic state generation
- Multi-agent simulation via `SimulatorHub`
- Agent memory and JSON persistence
- CLI and GUI interfaces
- Real-time visualizations
- GitHub Actions for automated testing

## 🚀 Quick Start

```bash
# Clone and install
git clone <your-repo-url>
cd AgentSim_v3
pip install -e .

# Run the simulation
python agent_sim/run_sim.py

# Launch GUI (optional)
streamlit run agent_sim/app.py
```

## 🧪 Testing

```bash
pytest
```

## 🗃️ Project Structure

```
agent_sim/
│
├── agents/               # Agent definitions (base, RL)
├── world/                # Environment/State generator
├── memory/               # Memory bank and JSON tools
├── utils/                # Visualization tools
├── data/                 # Logs and outputs
├── tests/                # Unit tests
├── run_sim.py            # CLI runner
├── app.py                # Streamlit GUI
└── simulator_hub.py      # Main orchestrator
```

## 📦 CI Pipeline

Included in `.github/workflows/test.yml`, runs lint and unit tests on every push/pull.

---

© 2025 AgentSim Dev Team

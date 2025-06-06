from setuptools import setup, find_packages

setup(
    name='AgentSim',
    version='0.1.0',
    description='A modular, scalable free-will agent simulation framework',
    author='AgentSim Dev Team',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'plotly',
        'pandas',
        'streamlit',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'agent-sim=agent_sim.run_sim:main'
        ]
    },
    python_requires='>=3.8',
)

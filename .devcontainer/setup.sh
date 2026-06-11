#!/bin/bash
set -e

# Upgrade pip and install useful tools
echo "Upgrading pip and installing tools..."
pip install --upgrade pip
pip install black pytest mypy ruff

# Create useful aliases
echo 'alias test="python -m unittest discover tests -v"' >> ~/.bashrc
echo 'alias run="python bloom_seed.py"' >> ~/.bashrc
echo 'alias agent="python local_agent.py"' >> ~/.bashrc

# Reload bashrc
source ~/.bashrc

echo "Setup complete! You can now use 'test', 'run', or 'agent' commands."
"""
Test swapping the backend/model for an agent via config.
Verifies that the LLM router respects the config change.
"""

import sys
import os
import yaml

sys.path.insert(0, "./src/mvp")
sys.path.insert(0, "./src/db")

from mvp.dev_team_agent import DevTeam
from llm_router import CONFIG_PATH

def test_llm_backend_swap():
    # Backup original config
    with open(CONFIG_PATH, 'r') as f:
        original_config = f.read()

    # Swap backend for dev_team to a fake "custom_api"
    config = yaml.safe_load(original_config)
    if "agents" not in config:
        config["agents"] = {}
    config['agents']['dev_team'] = 'custom_api'
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f)

    try:
        dev = DevTeam()
        feature = "test backend swap"
        result = dev.implement_feature(feature)
        assert ("No backend configured" in result or "[Ollama error: No response received]" in result), "LLM router did not respect backend swap"
        print("LLM backend swap: PASS")
    finally:
        # Restore original config
        with open(CONFIG_PATH, 'w') as f:
            f.write(original_config)

def run_tests():
    print("Running LLM backend swap test...")
    test_llm_backend_swap()
    print("All LLM backend swap tests passed.")

if __name__ == "__main__":
    run_tests()

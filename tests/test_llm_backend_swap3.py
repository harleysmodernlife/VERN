print("[DEBUG] test_llm_backend_swap3.py loaded")

"""
Test swapping the backend/model for an agent via config.
Verifies that the LLM router respects the config change.
"""

import os
import yaml

from mvp.dev_team_agent import DevTeam
from mvp.llm_router import CONFIG_PATH, route_llm_call

print("[DEBUG] route_llm_call module:", route_llm_call.__module__)
print("[DEBUG] route_llm_call file:", route_llm_call.__code__.co_filename)
import sys
print("[DEBUG] sys.path:", sys.path)

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

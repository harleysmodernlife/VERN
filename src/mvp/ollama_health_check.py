"""
Ollama Health Check Script for VERN

Checks if the Ollama service is running and if the configured model is available.
"""

import subprocess
import sys

OLLAMA_MODEL = "qwen3:0.6b"

def check_ollama_service():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("Ollama service not running or not found in PATH.")
            return False
        return True
    except Exception as e:
        print(f"Error checking Ollama service: {e}")
        return False

def check_model_available(model_name):
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        if model_name in result.stdout:
            return True
        else:
            print(f"Model '{model_name}' not found in Ollama. Run: ollama pull {model_name}")
            return False
    except Exception as e:
        print(f"Error checking model: {e}")
        return False

if __name__ == "__main__":
    print("Checking Ollama service...")
    if not check_ollama_service():
        sys.exit(1)
    print("Checking model availability...")
    if not check_model_available(OLLAMA_MODEL):
        sys.exit(2)
    print(f"Ollama service and model '{OLLAMA_MODEL}' are healthy.")

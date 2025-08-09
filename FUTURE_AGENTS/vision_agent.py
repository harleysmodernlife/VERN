"""
VERN Vision Agent

Handles image/document analysis for multimodal agent workflows.
Config-driven backend selection and resource-aware fallback.
"""

import yaml
import os
import psutil

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config/agent_backends.yaml')
def load_agent_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

AGENT_CONFIG = load_agent_config()

def check_resources(min_ram_gb=2, min_cpu_cores=2, require_gpu=False):
    ram_ok = psutil.virtual_memory().available / (1024 ** 3) >= min_ram_gb
    physical = psutil.cpu_count(logical=False)
    logical = psutil.cpu_count(logical=True) or 1
    cpu_cores = physical if isinstance(physical, int) and physical > 0 else logical
    cpu_ok = cpu_cores >= min_cpu_cores
    gpu_ok = True
    if require_gpu:
        # CPU-only environment: GPU/CUDA not supported
        print("Warning: GPU/CUDA requested but not available on this hardware. Running in CPU-only mode.")
        gpu_ok = False
    return ram_ok and cpu_ok and gpu_ok

def get_vision_backend(agent_name=None):
    if agent_name and 'vision_agents' in AGENT_CONFIG and agent_name in AGENT_CONFIG['vision_agents']:
        backend_key = AGENT_CONFIG['vision_agents'][agent_name]
    else:
        backend_key = AGENT_CONFIG.get('default_vision', 'tesseract')
    backend = AGENT_CONFIG['vision_backends'].get(backend_key)
    if backend is None:
        return None, None
    return backend.get('provider', 'tesseract'), backend.get('model', 'default')

import pytesseract
from PIL import Image
import io

# Image analysis stub
def analyze_image(image_bytes: bytes) -> dict:
    # Stub: Use CLIP, BLIP, or similar for image captioning/classification
    print("[VISION] Analyzing image...")
    return {"caption": "Image caption (stub)", "labels": ["label1", "label2"]}

def extract_text_from_document(doc_bytes: bytes, agent_name=None) -> str:
    """
    Extracts text from document image bytes using selected vision backend (config-driven, resource-aware).
    Falls back gracefully if preferred backend unavailable or resources are low.
    """
    provider, model = get_vision_backend(agent_name)
    print(f"[VISION] Extracting text from document with backend: {provider} ({model})")
    if provider == "tesseract" and check_resources(min_ram_gb=1, min_cpu_cores=1):
        try:
            image = Image.open(io.BytesIO(doc_bytes))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"[VISION] Tesseract OCR failed: {e}")
    elif provider == "google":
        # Stub: Google Vision API integration
        print("[VISION] Using Google Vision API (stub)")
        return "[Google Vision API not implemented]"
    # Fallback to stub
    print("[VISION] Falling back to stub OCR.")
    return "[OCR error: No backend available]"

# Example usage:
# result = analyze_image(b"...")
# text = extract_text_from_document(b"...")

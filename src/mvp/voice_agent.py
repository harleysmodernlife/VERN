"""
VERN Voice Agent

Handles voice input/output (ASR/TTS) for multimodal agent workflows.
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
    cpu_ok = psutil.cpu_count(logical=False) >= min_cpu_cores
    gpu_ok = True
    if require_gpu:
        try:
            import torch
            gpu_ok = torch.cuda.is_available()
        except ImportError:
            gpu_ok = False
    return ram_ok and cpu_ok and gpu_ok

def get_asr_backend(agent_name=None):
    if agent_name and 'asr_agents' in AGENT_CONFIG and agent_name in AGENT_CONFIG['asr_agents']:
        backend_key = AGENT_CONFIG['asr_agents'][agent_name]
    else:
        backend_key = AGENT_CONFIG.get('default_asr', 'whisper-base')
    backend = AGENT_CONFIG['asr_backends'].get(backend_key)
    if backend is None:
        return None, None
    return backend.get('provider', 'whisper'), backend.get('model', 'base')

def get_tts_backend(agent_name=None):
    if agent_name and 'tts_agents' in AGENT_CONFIG and agent_name in AGENT_CONFIG['tts_agents']:
        backend_key = AGENT_CONFIG['tts_agents'][agent_name]
    else:
        backend_key = AGENT_CONFIG.get('default_tts', 'coqui-tts')
    backend = AGENT_CONFIG['tts_backends'].get(backend_key)
    if backend is None:
        return None, None
    return backend.get('provider', 'coqui'), backend.get('model', 'tts_models/en/ljspeech/tacotron2-DDC')

import whisper
import tempfile

def transcribe_audio(audio_bytes: bytes, agent_name=None) -> str:
    """
    Transcribes audio bytes using selected ASR backend (config-driven, resource-aware).
    Falls back gracefully if preferred backend unavailable or resources are low.
    """
    provider, model = get_asr_backend(agent_name)
    print(f"[VOICE] Transcribing audio with ASR backend: {provider} ({model})")
    # Resource check: Whisper needs ~2GB RAM, 2 CPU cores
    if provider == "whisper" and check_resources(min_ram_gb=2, min_cpu_cores=2):
        try:
            import whisper
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio.flush()
                whisper_model = whisper.load_model(model)
                result = whisper_model.transcribe(temp_audio.name)
                return result["text"]
        except ImportError:
            print("[VOICE] Whisper not installed, falling back to stub ASR.")
            return "[ASR stub: Whisper not installed]"
        except Exception as e:
            print(f"[VOICE] Whisper ASR failed: {e}")
            return "[ASR stub: Whisper error]"
    elif provider == "google":
        # Stub: Google Speech API integration
        print("[VOICE] Using Google Speech API (stub)")
        return "[Google Speech API not implemented]"
    elif provider == "espeak":
        # Stub: Espeak ASR integration
        print("[VOICE] Using Espeak ASR (stub)")
        return "[Espeak ASR not implemented]"
    # Fallback to stub ASR if no backend available
    print("[VOICE] Falling back to stub ASR.")
    return "[ASR stub: No backend available]"

from TTS.api import TTS

def synthesize_speech(text: str, agent_name=None) -> bytes:
    """
    Synthesizes speech using selected TTS backend (config-driven, resource-aware).
    Falls back gracefully if preferred backend unavailable or resources are low.
    """
    provider, model = get_tts_backend(agent_name)
    print(f"[VOICE] Synthesizing speech with TTS backend: {provider} ({model})")
    # Resource check: Coqui needs ~2GB RAM, 2 CPU cores
    if provider == "coqui" and check_resources(min_ram_gb=2, min_cpu_cores=2):
        try:
            from TTS.api import TTS
            tts = TTS(model, progress_bar=False)
            wav = tts.tts(text)
            import numpy as np
            import io
            import soundfile as sf
            buf = io.BytesIO()
            sf.write(buf, wav, samplerate=22050, format='WAV', subtype='PCM_16')
            buf.seek(0)
            return buf.read()
        except Exception as e:
            print(f"[VOICE] Coqui TTS failed: {e}")
    elif provider == "google":
        # Stub: Google TTS API integration
        print("[VOICE] Using Google TTS API (stub)")
        return b"[Google TTS API not implemented]"
    elif provider == "espeak":
        # Stub: Espeak TTS integration
        print("[VOICE] Using Espeak TTS (stub)")
        return b"[Espeak TTS not implemented]"
    # Fallback to Espeak TTS (stub)
    print("[VOICE] Falling back to Espeak TTS (stub)")
    return b"[TTS error: No backend available]"

# Example usage:
# text = transcribe_audio(b"...")
# audio = synthesize_speech("Hello world")

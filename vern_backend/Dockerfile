# vern_backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY vern_backend/requirements.txt .
# Install only CPU-only PyTorch if needed, never GPU/CUDA by default
# Install CPU-only PyTorch first to avoid GPU/CUDA wheels
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN pip install -e .

ENV PYTHONPATH=/app:/app/src

# The FastAPI app is at vern_backend/app/main.py where 'app' is defined.
# Use module path 'vern_backend.app.main:app' instead of 'app/main:app'
CMD ["uvicorn", "vern_backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

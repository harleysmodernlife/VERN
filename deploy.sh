#!/bin/bash
# VERN Deployment Script

# Default ports (can be overridden by env or args)
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"
NEO4J_PORT="${NEO4J_PORT:-7687}"

# Accept positional arguments for ports
if [ ! -z "$1" ]; then BACKEND_PORT="$1"; fi
if [ ! -z "$2" ]; then FRONTEND_PORT="$2"; fi
if [ ! -z "$3" ]; then NEO4J_PORT="$3"; fi

# Environment variables
export BACKEND_PORT
export FRONTEND_PORT
export NEO4J_PORT
export NEO4J_URI="bolt://localhost:$NEO4J_PORT"
export NEO4J_USER="${NEO4J_USER:-neo4j}"
export NEO4J_PASSWORD="${NEO4J_PASSWORD:-test}"

echo "Starting Neo4j service..."
sudo systemctl start neo4j
sleep 5

echo "Starting VERN Backend..."
cd vern_backend || exit
source ../venv/bin/activate
uvicorn app.main:app --reload --port $BACKEND_PORT &
BACKEND_PID=$!
cd ..

echo "Starting VERN Frontend..."
cd vern_frontend || exit
PORT=$FRONTEND_PORT npm run dev &
FRONTEND_PID=$!
cd ..

echo "VERN backend running at http://localhost:$BACKEND_PORT"
echo "VERN frontend running at http://localhost:$FRONTEND_PORT"
echo "Neo4j running at bolt://localhost:$NEO4J_PORT"
echo "Press Ctrl+C to stop all servers."

echo "Running smoke tests..."
bash scripts/smoke.sh

trap 'kill $BACKEND_PID $FRONTEND_PID' EXIT
wait

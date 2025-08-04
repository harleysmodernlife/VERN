#!/bin/bash
# VERN Deployment Script

echo "Starting VERN Backend..."
cd vern_backend || exit
source ../venv/bin/activate
uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

echo "Starting VERN Frontend..."
cd vern_frontend || exit
npm run dev &
FRONTEND_PID=$!
cd ..

echo "VERN backend running at http://localhost:8000"
echo "VERN frontend running at http://localhost:3000"
echo "Press Ctrl+C to stop both servers."

trap 'kill $BACKEND_PID $FRONTEND_PID' EXIT
wait

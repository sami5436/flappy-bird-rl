#!/bin/bash
# Quick test to verify the game server and visualization work

echo "Testing game server with demo..."
echo "This will run a simple demo. Start the Java GUI in another terminal to see it work."
echo ""
echo "To start Java GUI:"
echo "  cd java"
echo "  java -cp .:json-20230227.jar:src FlappyBirdGUI"
echo ""
read -p "Press Enter to start the demo server, or Ctrl+C to cancel..."

cd python
python game_server.py

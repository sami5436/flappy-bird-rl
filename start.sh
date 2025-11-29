#!/bin/bash
# Quick start script for Flappy Bird DQN training

echo "========================================="
echo "Flappy Bird DQN - Quick Start"
echo "========================================="
echo ""

# Check if Python dependencies are installed
echo "Checking Python dependencies..."
python -c "import torch; import numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing Python dependencies..."
    pip install -r python/requirements.txt
fi

echo ""
echo "Choose a mode:"
echo "1) Train without visualization (fastest)"
echo "2) Train with visualization (requires Java GUI)"
echo "3) Watch trained model play (requires Java GUI and trained model)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting training without visualization..."
        echo "This is the fastest way to train the agent."
        echo ""
        cd python
        python train.py --episodes 1000
        ;;
    2)
        echo ""
        echo "Starting training WITH visualization..."
        echo ""
        echo "IMPORTANT: You need to start the Java GUI in another terminal:"
        echo "  cd java"
        echo "  java -cp .:json-20230227.jar:src FlappyBirdGUI"
        echo ""
        read -p "Press Enter when Java GUI is ready, or Ctrl+C to cancel..."
        cd python
        python train.py --episodes 1000 --visualize
        ;;
    3)
        if [ ! -f "models/best_model.pth" ]; then
            echo ""
            echo "Error: No trained model found at models/best_model.pth"
            echo "Please train a model first using option 1 or 2."
            exit 1
        fi
        echo ""
        echo "Starting playback mode..."
        echo ""
        echo "IMPORTANT: You need to start the Java GUI in another terminal:"
        echo "  cd java"
        echo "  java -cp .:json-20230227.jar:src FlappyBirdGUI"
        echo ""
        read -p "Press Enter when Java GUI is ready, or Ctrl+C to cancel..."
        cd python
        python train.py --mode play --load-model models/best_model.pth --visualize --episodes 5
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

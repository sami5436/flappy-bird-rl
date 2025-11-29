#!/bin/bash
# Compile Java GUI for Flappy Bird

echo "Compiling Java GUI..."
cd java
javac -cp .:json-20230227.jar src/*.java

if [ $? -eq 0 ]; then
    echo "✓ Compilation successful!"
    echo ""
    echo "To run the GUI:"
    echo "  cd java"
    echo "  java -cp .:json-20230227.jar:src FlappyBirdGUI"
else
    echo "✗ Compilation failed"
    echo ""
    echo "Make sure you have Java JDK installed:"
    echo "  brew install openjdk"
    exit 1
fi

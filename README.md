# Flappy Bird with DQN Reinforcement Learning

A Flappy Bird game implementation with Deep Q-Network (DQN) reinforcement learning. The game logic and AI training are implemented in **Python**, while the visualization uses a **Java Swing GUI**. The two components communicate via socket-based JSON protocol.

## Architecture

```
┌─────────────────────┐         Socket (JSON)        ┌──────────────────┐
│  Python Backend     │◄────────────────────────────►│   Java GUI       │
│                     │        localhost:5000        │                  │
│  - Game Logic       │                              │  - Visualization │
│  - Physics Engine   │                              │  - Rendering     │
│  - DQN Training     │                              │  - Window Mgmt   │
│  - State Management │                              │                  │
└─────────────────────┘                              └──────────────────┘
```

## Features

- **DQN Agent**: Deep Q-Network implementation using PyTorch
- **Experience Replay**: 10,000 transition buffer for stable training
- **Target Network**: Periodic updates for training stability
- **Real-time Visualization**: Java Swing GUI displays training/playback
- **Multiple Modes**: Train with/without visualization, play trained models
- **Model Persistence**: Save and load trained models

## Requirements

### Python
- Python 3.7+
- PyTorch
- NumPy

### Java
- JDK 8 or higher
- org.json library (included)

## Setup

### 1. Install Python Dependencies

```bash
cd python
pip install -r requirements.txt
```

### 2. Verify Java Installation

```bash
java -version
javac -version
```

## Usage

### Training the DQN Agent

#### Train without visualization (fastest)
```bash
cd python
python train.py --episodes 1000
```

#### Train WITH visualization
```bash
# Terminal 1: Start Python training with visualization server
cd python
python train.py --episodes 1000 --visualize

# Terminal 2: Start Java GUI (in a new terminal)
cd java
javac -cp .:json-20230227.jar src/*.java
java -cp .:json-20230227.jar:src FlappyBirdGUI
```

#### Resume training from checkpoint
```bash
cd python
python train.py --episodes 2000 --load-model models/checkpoint_ep1000.pth
```

### Playing with a Trained Model

```bash
# Terminal 1: Start Python in play mode
cd python
python train.py --mode play --load-model models/best_model.pth --visualize --episodes 10

# Terminal 2: Start Java GUI
cd java
java -cp .:json-20230227.jar:src FlappyBirdGUI
```

### Training Options

```
--mode {train,play}     Mode: train or play (default: train)
--episodes N            Number of episodes (default: 1000)
--visualize             Enable visualization with Java GUI
--load-model PATH       Path to model to load
--save-freq N           Save checkpoint every N episodes (default: 100)
--fps N                 Visualization FPS (default: 60)
```

## How It Works

### Game Environment
- **State Space**: Bird Y position, velocity, distance to next pipe, gap position
- **Action Space**: {0: Do nothing, 1: Flap}
- **Rewards**: 
  - +0.1 per frame survived
  - +1.0 for passing a pipe
  - -10.0 for collision

### DQN Architecture
- **Input**: 4-dimensional state vector
- **Network**: 3-layer fully connected (4 → 128 → 64 → 2)
- **Algorithm**: Double DQN with experience replay
- **Hyperparameters**:
  - Learning rate: 0.001
  - Gamma (discount): 0.99
  - Epsilon decay: 0.995 (1.0 → 0.01)
  - Batch size: 64
  - Target network update: Every 10 episodes

### Communication Protocol

Python server sends JSON game state at 60 FPS:

```json
{
  "bird": {
    "x": 150,
    "y": 300,
    "velocity": -2.5
  },
  "pipes": [
    {
      "x": 400,
      "gap_y": 250,
      "gap_size": 200,
      "width": 80
    }
  ],
  "score": 5,
  "game_over": false,
  "width": 800,
  "height": 600
}
```

## Project Structure

```
flappy-bird/
├── python/
│   ├── game_env.py       # Flappy Bird game environment
│   ├── dqn_agent.py      # DQN agent implementation
│   ├── train.py          # Training and play script
│   ├── game_server.py    # Socket server for GUI
│   └── requirements.txt  # Python dependencies
├── java/
│   ├── src/
│   │   ├── FlappyBirdGUI.java  # Main window
│   │   ├── GamePanel.java      # Rendering panel
│   │   └── GameClient.java     # Socket client
│   └── json-20230227.jar       # JSON library
└── models/               # Saved model checkpoints
    ├── best_model.pth
    ├── final_model.pth
    └── checkpoint_ep*.pth
```

## Training Tips

1. **Start with visualization**: Train for 100-200 episodes with `--visualize` to verify everything works
2. **Fast training**: Disable visualization for long training runs (1000+ episodes)
3. **Monitor progress**: The agent should start scoring consistently after 200-500 episodes
4. **Best scores**: Well-trained agents can score 50-100+ points
5. **Checkpoints**: Models are saved every 100 episodes by default

## Troubleshooting

**Java GUI shows "Waiting for Python server..."**
- Make sure Python training is running with `--visualize` flag
- Check that port 5000 is not blocked by firewall

**"Connection refused" error**
- Python server must be started before Java GUI
- Wait a few seconds after starting Python before launching Java GUI

**Poor training performance**
- Try training for more episodes (1000+)
- Adjust hyperparameters in `dqn_agent.py`
- Check that rewards are balanced (modify in `game_env.py`)

**Java compilation errors**
- Ensure JSON library is in the same directory as source files
- Use correct classpath: `-cp .:json-20230227.jar`

## Example Training Session

```bash
# Start training
$ cd python
$ python train.py --episodes 500 --visualize

============================================================
Starting training for 500 episodes
Visualization: ON
============================================================

Using device: cpu
Game server started on localhost:5000
Waiting for Java GUI to connect...

Episode   10 | Score:   0 | Avg Score:   0.00 | Best:   0 | Epsilon: 0.951 | Loss: 0.0234
Episode   20 | Score:   1 | Avg Score:   0.15 | Best:   1 | Epsilon: 0.904 | Loss: 0.0189
Episode   30 | Score:   2 | Avg Score:   0.40 | Best:   3 | Epsilon: 0.860 | Loss: 0.0156
...
Episode  500 | Score:  45 | Avg Score:  32.10 | Best:  67 | Epsilon: 0.010 | Loss: 0.0023

============================================================
Training completed!
Best score: 67
Final model saved to models/final_model.pth
============================================================
```

## License

This project is for educational purposes.

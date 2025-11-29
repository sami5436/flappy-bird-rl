# 🎯 Optimized Training Parameters for Flappy Bird DQN

## The Problem: Bird Hits Ceiling

You observed the bird constantly hitting the ceiling. This is because:
1. **Flap strength too strong** (-9 is very powerful)
2. **No penalty for flapping** (encourages spam)
3. **Reward only for survival** (doesn't discourage bad actions)

## The Solution: Tuned Parameters

### Quick Fix (Easiest)

Edit `python/game_env.py` line 18:
```python
# BEFORE:
self.FLAP_STRENGTH = -9

# AFTER (gentler flap):
self.FLAP_STRENGTH = -7
```

### Better Reward Shaping

Edit `python/game_env.py` around lines 79-100:

**Current rewards:**
- Survive: +0.1
- Hit ceiling/floor: -10
- Pass pipe: +1

**Improved rewards** (add this logic):
```python
# After line 99, replace reward calculation with:

# Start with small survival reward
reward = 0.1

# Small penalty for flapping (discourage spam)
if action == 1:
    reward -= 0.05

# Penalty for being too close to ceiling or floor
if self.bird_y < 100 or self.bird_y > self.HEIGHT - 100:
    reward -= 0.05

# Big penalty for collision
if self.bird_y < 0 or self.bird_y > self.HEIGHT:
    reward = -10
    done = True
    self.game_over = True

# Pipe collision (existing code stays)
# ... pipe collision check ...

# Big reward for passing pipe
if pipe_passed:
    reward = 2.0  # Increased from 1.0
```

## Training Tips

### 1. Train Longer
The bird needs ~500-1000 episodes to learn properly:
```bash
cd python
python train.py --episodes 2000
```

### 2. Speed Up Training
Train WITHOUT visualization (10x faster):
```bash
python train.py --episodes 2000
```

### 3. Watch Progress
Every 200 episodes, test your model:
```bash
# In another terminal after checkpoints are saved
python train.py --mode play --load-model models/checkpoint_ep200.pth --visualize --episodes 3
```

## Expected Learning Curve

| Episodes | Behavior | Avg Score |
|----------|----------|-----------|
| 0-100 | Random flapping, hits ceiling | 0 |
| 100-300 | Learns to not spam flap | 0-2 |
| 300-500 | Occasional pipe pass | 2-10 |
| 500-1000 | Consistent play | 10-30 |
| 1000+ | Expert play | 30-100+ |

## Quick Parameter Reference

**Physics (in `game_env.py`):**
- `GRAVITY = 0.5` ✅ Good
- `FLAP_STRENGTH = -7` ⬅️ **Change from -9**
- `PIPE_SPEED = 3` ✅ Good
- `PIPE_GAP = 200` ✅ Good

**DQN (in `dqn_agent.py`):**
- `learning_rate = 0.001` ✅ Good
- `gamma = 0.99` ✅ Good
- `epsilon_decay = 0.995` ✅ Good
- `batch_size = 64` ✅ Good

## Try This Now

**Option 1: Just reduce flap strength (1 line change)**
```bash
# Edit python/game_env.py line 18
# Change FLAP_STRENGTH from -9 to -7
```

**Option 2: Full optimization (I can make these changes for you)**
- Reduce flap strength
- Add flap penalty
- Add ceiling/floor proximity penalty
- Increase pipe-passing reward

Which would you prefer? I can make the changes automatically! 🚀

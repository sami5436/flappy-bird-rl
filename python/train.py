"""
Training script for Flappy Bird DQN Agent
Supports training with/without visualization and loading pre-trained models
"""
import argparse
import time
import os
import numpy as np
from game_env import FlappyBirdEnv
from dqn_agent import DQNAgent
from game_server import GameServer


def train(episodes=1000, visualize=False, load_model=None, save_freq=100, render_fps=60):
    """
    Train DQN agent on Flappy Bird
    
    Args:
        episodes: Number of episodes to train
        visualize: Whether to send state to Java GUI
        load_model: Path to pre-trained model to load
        save_freq: Save model every N episodes
        render_fps: FPS for visualization (if enabled)
    """
    # Initialize environment and agent
    env = FlappyBirdEnv()
    agent = DQNAgent(state_size=4, action_size=2)
    
    # Get project root directory (parent of python folder)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load pre-trained model if specified
    if load_model:
        if not os.path.isabs(load_model):
            load_model = os.path.join(project_root, load_model)
        if os.path.exists(load_model):
            agent.load(load_model)
    
    # Start visualization server if requested
    server = None
    if visualize:
        server = GameServer()
        server.start()
        print("\nWaiting for Java GUI to connect...")
        print("Start the Java GUI with: cd java && java -cp .:json-20230227.jar:src FlappyBirdGUI\n")
        time.sleep(2)  # Give server time to start
    
    # Training loop
    best_score = 0
    scores = []
    losses = []
    frame_time = 1.0 / render_fps if visualize else 0
    
    print(f"\n{'='*60}")
    print(f"Starting training for {episodes} episodes")
    print(f"Visualization: {'ON' if visualize else 'OFF'}")
    print(f"{'='*60}\n")
    
    try:
        for episode in range(1, episodes + 1):
            state = env.reset()
            done = False
            episode_reward = 0
            episode_losses = []
            
            while not done:
                # Select and perform action
                action = agent.select_action(state, training=True)
                next_state, reward, done, info = env.step(action)
                
                # Store transition
                agent.store_transition(state, action, reward, next_state, done)
                
                # Train agent
                loss = agent.train_step()
                if loss is not None:
                    episode_losses.append(loss)
                
                episode_reward += reward
                state = next_state
                
                # Send state to GUI if visualizing
                if visualize and server:
                    server.send_state(env.get_game_state_dict())
                    if frame_time > 0:
                        time.sleep(frame_time)
            
            # Update epsilon and target network
            agent.update_epsilon()
            
            # Track statistics
            scores.append(env.score)
            avg_loss = np.mean(episode_losses) if episode_losses else 0
            losses.append(avg_loss)
            
            # Update best score
            if env.score > best_score:
                best_score = env.score
                # Save best model
                models_dir = os.path.join(project_root, 'models')
                os.makedirs(models_dir, exist_ok=True)
                agent.save(os.path.join(models_dir, 'best_model.pth'))
            
            # Print progress
            if episode % 10 == 0:
                avg_score = np.mean(scores[-100:]) if len(scores) >= 100 else np.mean(scores)
                avg_loss = np.mean(losses[-100:]) if len(losses) >= 100 else np.mean(losses)
                print(f"Episode {episode:4d} | "
                      f"Score: {env.score:3d} | "
                      f"Avg Score: {avg_score:6.2f} | "
                      f"Best: {best_score:3d} | "
                      f"Epsilon: {agent.epsilon:.3f} | "
                      f"Loss: {avg_loss:.4f}")
            
            # Save checkpoint periodically
            if episode % save_freq == 0:
                models_dir = os.path.join(project_root, 'models')
                os.makedirs(models_dir, exist_ok=True)
                agent.save(os.path.join(models_dir, f'checkpoint_ep{episode}.pth'))
                print(f"→ Checkpoint saved at episode {episode}")
    
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user")
    
    finally:
        # Save final model
        models_dir = os.path.join(project_root, 'models')
        os.makedirs(models_dir, exist_ok=True)
        agent.save(os.path.join(models_dir, 'final_model.pth'))
        print(f"\n{'='*60}")
        print(f"Training completed!")
        print(f"Best score: {best_score}")
        print(f"Final model saved to models/final_model.pth")
        print(f"{'='*60}\n")
        
        # Stop server
        if server:
            server.stop()


def play(model_path, num_episodes=5, visualize=True):
    """
    Play Flappy Bird with a trained model
    
    Args:
        model_path: Path to trained model
        num_episodes: Number of episodes to play
        visualize: Whether to send state to Java GUI
    """
    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Handle relative paths
    if not os.path.isabs(model_path):
        model_path = os.path.join(project_root, model_path)
    
    env = FlappyBirdEnv()
    agent = DQNAgent(state_size=4, action_size=2)
    
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return
    
    agent.load(model_path)
    agent.epsilon = 0  # No exploration during play
    
    # Start visualization server if requested
    server = None
    if visualize:
        server = GameServer()
        server.start()
        print("\nWaiting for Java GUI to connect...")
        print("Start the Java GUI with: cd java && java -cp .:json-20230227.jar:src FlappyBirdGUI\n")
        time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"Playing {num_episodes} episodes with trained model")
    print(f"{'='*60}\n")
    
    scores = []
    
    try:
        for episode in range(1, num_episodes + 1):
            state = env.reset()
            done = False
            
            while not done:
                action = agent.select_action(state, training=False)
                state, reward, done, info = env.step(action)
                
                if visualize and server:
                    server.send_state(env.get_game_state_dict())
                    time.sleep(1/60)  # 60 FPS
            
            scores.append(env.score)
            print(f"Episode {episode}: Score = {env.score}")
        
        print(f"\nAverage Score: {np.mean(scores):.2f}")
        print(f"Best Score: {max(scores)}")
    
    except KeyboardInterrupt:
        print("\n\nPlayback interrupted by user")
    
    finally:
        if server:
            server.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train or play Flappy Bird with DQN')
    parser.add_argument('--mode', type=str, default='train', choices=['train', 'play'],
                        help='Mode: train or play')
    parser.add_argument('--episodes', type=int, default=1000,
                        help='Number of episodes (default: 1000)')
    parser.add_argument('--visualize', action='store_true',
                        help='Enable visualization with Java GUI')
    parser.add_argument('--load-model', type=str, default=None,
                        help='Path to model to load')
    parser.add_argument('--save-freq', type=int, default=100,
                        help='Save checkpoint every N episodes (default: 100)')
    parser.add_argument('--fps', type=int, default=60,
                        help='Visualization FPS (default: 60)')
    
    args = parser.parse_args()
    
    if args.mode == 'train':
        train(
            episodes=args.episodes,
            visualize=args.visualize,
            load_model=args.load_model,
            save_freq=args.save_freq,
            render_fps=args.fps
        )
    else:  # play mode
        if args.load_model is None:
            args.load_model = 'models/best_model.pth'
        play(
            model_path=args.load_model,
            num_episodes=args.episodes,
            visualize=args.visualize
        )

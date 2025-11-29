"""
Flappy Bird Game Environment
OpenAI Gym-style interface for DQN training
"""
import numpy as np
import random
import math


class FlappyBirdEnv:
    """Flappy Bird environment with simple physics"""
    
    def __init__(self):
        # Game constants
        self.WIDTH = 800
        self.HEIGHT = 600
        self.GRAVITY = 0.5
        self.FLAP_STRENGTH = -7  # Reduced from -9 to prevent ceiling spam
        self.BIRD_X = 150
        self.PIPE_WIDTH = 80
        self.PIPE_GAP = 200
        self.PIPE_SPEED = 3
        self.PIPE_SPACING = 300
        
        # State variables
        self.reset()
        
    def reset(self):
        """Reset the game to initial state"""
        self.bird_y = self.HEIGHT // 2
        self.bird_velocity = 0
        self.score = 0
        self.game_over = False
        self.frames = 0
        
        # Initialize pipes: [(x, gap_y), ...]
        # gap_y is the center of the gap
        self.pipes = []
        for i in range(3):
            x = self.WIDTH + i * self.PIPE_SPACING
            gap_y = random.randint(150, self.HEIGHT - 150)
            self.pipes.append([x, gap_y])
            
        return self._get_state()
    
    def _get_state(self):
        """Get current state as numpy array for neural network"""
        # Find the next pipe ahead of the bird
        next_pipe = None
        for pipe in self.pipes:
            if pipe[0] + self.PIPE_WIDTH > self.BIRD_X:
                next_pipe = pipe
                break
        
        if next_pipe is None:
            next_pipe = self.pipes[0]
        
        # Normalize state values
        state = np.array([
            self.bird_y / self.HEIGHT,  # Bird y position (0-1)
            self.bird_velocity / 10,    # Bird velocity (-1 to 1 roughly)
            (next_pipe[0] - self.BIRD_X) / self.WIDTH,  # Distance to next pipe
            next_pipe[1] / self.HEIGHT,  # Gap center position
        ], dtype=np.float32)
        
        return state
    
    def step(self, action):
        """
        Execute one step in the environment
        action: 0 = do nothing, 1 = flap
        Returns: (state, reward, done, info)
        """
        if self.game_over:
            return self._get_state(), 0, True, {}
        
        self.frames += 1
        
        # Apply action
        if action == 1:
            self.bird_velocity = self.FLAP_STRENGTH
        
        # Apply physics
        self.bird_velocity += self.GRAVITY
        self.bird_y += self.bird_velocity
        
        # Move pipes
        for pipe in self.pipes:
            pipe[0] -= self.PIPE_SPEED
        
        # Remove off-screen pipes and add new ones
        if self.pipes[0][0] < -self.PIPE_WIDTH:
            self.pipes.pop(0)
            x = self.pipes[-1][0] + self.PIPE_SPACING
            gap_y = random.randint(150, self.HEIGHT - 150)
            self.pipes.append([x, gap_y])
        
        # Reward shaping (optimized to discourage ceiling spam)
        reward = 0.1  # Small reward for surviving
        done = False
        
        # Small penalty for flapping (discourages spam)
        if action == 1:
            reward -= 0.05
        
        # Penalty for being too close to ceiling or floor
        if self.bird_y < 80 or self.bird_y > self.HEIGHT - 80:
            reward -= 0.1
        
        # Check if bird hit floor or ceiling
        if self.bird_y < 0 or self.bird_y > self.HEIGHT:
            reward = -10
            done = True
            self.game_over = True
        
        # Check pipe collisions
        bird_rect = {
            'x': self.BIRD_X - 15,
            'y': self.bird_y - 15,
            'width': 30,
            'height': 30
        }
        
        for pipe in self.pipes:
            pipe_x = pipe[0]
            gap_y = pipe[1]
            
            # Check if bird is in pipe's x range
            if (bird_rect['x'] + bird_rect['width'] > pipe_x and 
                bird_rect['x'] < pipe_x + self.PIPE_WIDTH):
                
                # Check if bird is outside the gap
                gap_top = gap_y - self.PIPE_GAP // 2
                gap_bottom = gap_y + self.PIPE_GAP // 2
                
                if (bird_rect['y'] < gap_top or 
                    bird_rect['y'] + bird_rect['height'] > gap_bottom):
                    reward = -10
                    done = True
                    self.game_over = True
                    break
        
        # Check if bird passed a pipe (for scoring)
        for pipe in self.pipes:
            if (pipe[0] + self.PIPE_WIDTH < self.BIRD_X and 
                pipe[0] + self.PIPE_WIDTH > self.BIRD_X - self.PIPE_SPEED):
                self.score += 1
                reward = 2.0  # Increased reward for passing pipe (was 1.0)
        
        state = self._get_state()
        info = {'score': self.score, 'frames': self.frames}
        
        return state, reward, done, info
    
    def get_game_state_dict(self):
        """Get full game state for visualization (Java GUI)"""
        return {
            'bird': {
                'x': self.BIRD_X,
                'y': int(self.bird_y),
                'velocity': float(self.bird_velocity)
            },
            'pipes': [
                {
                    'x': int(pipe[0]),
                    'gap_y': int(pipe[1]),
                    'gap_size': self.PIPE_GAP,
                    'width': self.PIPE_WIDTH
                }
                for pipe in self.pipes
            ],
            'score': self.score,
            'game_over': self.game_over,
            'width': self.WIDTH,
            'height': self.HEIGHT
        }
    
    def test_random_agent(self, num_episodes=10):
        """Test environment with random actions"""
        print(f"Testing environment with {num_episodes} random episodes...")
        total_scores = []
        
        for episode in range(num_episodes):
            state = self.reset()
            done = False
            episode_reward = 0
            
            while not done:
                action = random.randint(0, 1)
                state, reward, done, info = self.step(action)
                episode_reward += reward
            
            total_scores.append(self.score)
            print(f"Episode {episode + 1}: Score = {self.score}, Reward = {episode_reward:.2f}")
        
        print(f"\nAverage score: {np.mean(total_scores):.2f}")
        print("Environment test completed successfully!")


if __name__ == "__main__":
    # Test the environment
    env = FlappyBirdEnv()
    env.test_random_agent(5)

"""
Game Server for visualizing Flappy Bird with Java GUI
Sends game state via socket connection as JSON
"""
import socket
import json
import threading
import time


class GameServer:
    """Socket server to broadcast game state to Java GUI"""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.server_thread = None
        
    def start(self):
        """Start the server in a separate thread"""
        self.running = True
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        print(f"Game server started on {self.host}:{self.port}")
        print("Waiting for Java GUI to connect...")
    
    def _run_server(self):
        """Run the server to accept connections"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.server_socket.settimeout(1.0)  # Timeout for checking running flag
            
            while self.running:
                try:
                    self.client_socket, addr = self.server_socket.accept()
                    print(f"Java GUI connected from {addr}")
                    self.client_socket.settimeout(0.1)
                    # Connection established, keep accepting new connections if this one drops
                    # The main loop will handle sending data via send_state()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Connection error: {e}")
                    # Reset client socket on error
                    self.client_socket = None
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def send_state(self, game_state_dict):
        """Send game state to connected client"""
        if self.client_socket:
            try:
                message = json.dumps(game_state_dict) + "\n"
                self.client_socket.sendall(message.encode())
            except (BrokenPipeError, ConnectionResetError, OSError):
                print("Client disconnected")
                self.client_socket = None
            except Exception as e:
                print(f"Error sending state: {e}")
                self.client_socket = None
    
    def is_connected(self):
        """Check if a client is connected"""
        return self.client_socket is not None
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        print("Game server stopped")


if __name__ == "__main__":
    # Test the server
    from game_env import FlappyBirdEnv
    
    print("Testing game server...")
    env = FlappyBirdEnv()
    server = GameServer()
    server.start()
    
    print("Server running. Connect Java GUI and press Ctrl+C to stop.")
    
    try:
        state = env.reset()
        while True:
            action = 0 if env.frames % 30 < 15 else 1  # Alternating flap
            state, reward, done, info = env.step(action)
            
            if done:
                state = env.reset()
            
            # Send state to GUI
            server.send_state(env.get_game_state_dict())
            time.sleep(1/60)  # 60 FPS
            
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()

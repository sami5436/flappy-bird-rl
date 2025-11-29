import java.io.*;
import java.net.*;
import org.json.*;

/**
 * Socket client to receive game state from Python server
 */
public class GameClient extends Thread {
    private String host;
    private int port;
    private Socket socket;
    private BufferedReader in;
    private GamePanel gamePanel;
    private boolean running;
    
    public GameClient(String host, int port, GamePanel gamePanel) {
        this.host = host;
        this.port = port;
        this.gamePanel = gamePanel;
        this.running = true;
    }
    
    @Override
    public void run() {
        while (running) {
            try {
                System.out.println("Connecting to Python server at " + host + ":" + port + "...");
                socket = new Socket(host, port);
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                System.out.println("Connected to Python server!");
                
                String line;
                while (running && (line = in.readLine()) != null) {
                    try {
                        JSONObject gameState = new JSONObject(line);
                        gamePanel.updateGameState(gameState);
                    } catch (JSONException e) {
                        System.err.println("Error parsing JSON: " + e.getMessage());
                    }
                }
                
            } catch (IOException e) {
                System.err.println("Connection error: " + e.getMessage());
                System.out.println("Retrying in 2 seconds...");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException ie) {
                    break;
                }
            } finally {
                closeConnection();
            }
        }
    }
    
    public void stopClient() {
        running = false;
        closeConnection();
    }
    
    private void closeConnection() {
        try {
            if (in != null) in.close();
            if (socket != null) socket.close();
        } catch (IOException e) {
            // Ignore
        }
    }
}

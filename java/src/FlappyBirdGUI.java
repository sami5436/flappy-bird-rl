import javax.swing.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

/**
 * Main GUI window for Flappy Bird visualization
 */
public class FlappyBirdGUI extends JFrame {
    private GamePanel gamePanel;
    private GameClient gameClient;
    
    public FlappyBirdGUI() {
        setTitle("Flappy Bird - DQN Visualization");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        
        // Create game panel
        gamePanel = new GamePanel();
        add(gamePanel);
        
        // Pack and center window
        pack();
        setLocationRelativeTo(null);
        setResizable(false);
        
        // Start game client
        gameClient = new GameClient("localhost", 5000, gamePanel);
        gameClient.start();
        
        // Cleanup on close
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                if (gameClient != null) {
                    gameClient.stopClient();
                }
            }
        });
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            FlappyBirdGUI gui = new FlappyBirdGUI();
            gui.setVisible(true);
            
            System.out.println("Flappy Bird GUI started!");
            System.out.println("Waiting for connection from Python server...");
            System.out.println("Start Python with: cd ../python && python train.py --visualize");
        });
    }
}

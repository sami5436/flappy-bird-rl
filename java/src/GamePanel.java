import javax.swing.*;
import java.awt.*;
import org.json.*;

/**
 * Game panel for rendering Flappy Bird
 */
public class GamePanel extends JPanel {
    private JSONObject gameState;
    private final Object lock = new Object();
    
    // Colors
    private final Color SKY_BLUE = new Color(135, 206, 250);
    private final Color BIRD_YELLOW = new Color(255, 215, 0);
    private final Color PIPE_GREEN = new Color(34, 139, 34);
    private final Color GROUND_BROWN = new Color(139, 90, 43);
    
    public GamePanel() {
        setPreferredSize(new Dimension(800, 600));
        setBackground(SKY_BLUE);
        
        // Start rendering loop
        Timer timer = new Timer(16, e -> repaint()); // ~60 FPS
        timer.start();
    }
    
    public void updateGameState(JSONObject newState) {
        synchronized (lock) {
            this.gameState = newState;
        }
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        
        // Enable anti-aliasing for smooth graphics
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        synchronized (lock) {
            if (gameState == null) {
                drawWaitingScreen(g2d);
                return;
            }
            
            try {
                // Draw pipes
                if (gameState.has("pipes")) {
                    JSONArray pipes = gameState.getJSONArray("pipes");
                    for (int i = 0; i < pipes.length(); i++) {
                        JSONObject pipe = pipes.getJSONObject(i);
                        drawPipe(g2d, pipe);
                    }
                }
                
                // Draw bird
                if (gameState.has("bird")) {
                    JSONObject bird = gameState.getJSONObject("bird");
                    drawBird(g2d, bird);
                }
                
                // Draw ground
                drawGround(g2d);
                
                // Draw score
                if (gameState.has("score")) {
                    int score = gameState.getInt("score");
                    drawScore(g2d, score);
                }
                
                // Draw game over
                if (gameState.has("game_over") && gameState.getBoolean("game_over")) {
                    drawGameOver(g2d);
                }
                
            } catch (JSONException e) {
                System.err.println("Error rendering game state: " + e.getMessage());
            }
        }
    }
    
    private void drawWaitingScreen(Graphics2D g2d) {
        g2d.setColor(Color.WHITE);
        g2d.setFont(new Font("Arial", Font.BOLD, 24));
        String msg = "Waiting for Python server...";
        FontMetrics fm = g2d.getFontMetrics();
        int x = (getWidth() - fm.stringWidth(msg)) / 2;
        int y = getHeight() / 2;
        g2d.drawString(msg, x, y);
        
        g2d.setFont(new Font("Arial", Font.PLAIN, 16));
        String msg2 = "Start Python with: python train.py --visualize";
        fm = g2d.getFontMetrics();
        x = (getWidth() - fm.stringWidth(msg2)) / 2;
        g2d.drawString(msg2, x, y + 30);
    }
    
    private void drawBird(Graphics2D g2d, JSONObject bird) throws JSONException {
        int x = bird.getInt("x");
        int y = bird.getInt("y");
        int size = 30;
        
        // Bird body (circle)
        g2d.setColor(BIRD_YELLOW);
        g2d.fillOval(x - size/2, y - size/2, size, size);
        
        // Bird outline
        g2d.setColor(Color.ORANGE);
        g2d.setStroke(new BasicStroke(2));
        g2d.drawOval(x - size/2, y - size/2, size, size);
        
        // Bird eye
        g2d.setColor(Color.BLACK);
        g2d.fillOval(x + 5, y - 5, 6, 6);
        
        // Beak
        g2d.setColor(Color.ORANGE);
        int[] beakX = {x + size/2, x + size/2 + 10, x + size/2};
        int[] beakY = {y - 3, y, y + 3};
        g2d.fillPolygon(beakX, beakY, 3);
    }
    
    private void drawPipe(Graphics2D g2d, JSONObject pipe) throws JSONException {
        int x = pipe.getInt("x");
        int gapY = pipe.getInt("gap_y");
        int gapSize = pipe.getInt("gap_size");
        int width = pipe.getInt("width");
        int height = getHeight();
        
        // Top pipe
        g2d.setColor(PIPE_GREEN);
        g2d.fillRect(x, 0, width, gapY - gapSize/2);
        
        // Top pipe border
        g2d.setColor(new Color(0, 100, 0));
        g2d.setStroke(new BasicStroke(3));
        g2d.drawRect(x, 0, width, gapY - gapSize/2);
        
        // Top pipe cap
        g2d.setColor(PIPE_GREEN);
        g2d.fillRect(x - 5, gapY - gapSize/2 - 20, width + 10, 20);
        g2d.setColor(new Color(0, 100, 0));
        g2d.drawRect(x - 5, gapY - gapSize/2 - 20, width + 10, 20);
        
        // Bottom pipe
        g2d.setColor(PIPE_GREEN);
        g2d.fillRect(x, gapY + gapSize/2, width, height - (gapY + gapSize/2));
        
        // Bottom pipe border
        g2d.setColor(new Color(0, 100, 0));
        g2d.drawRect(x, gapY + gapSize/2, width, height - (gapY + gapSize/2));
        
        // Bottom pipe cap
        g2d.setColor(PIPE_GREEN);
        g2d.fillRect(x - 5, gapY + gapSize/2, width + 10, 20);
        g2d.setColor(new Color(0, 100, 0));
        g2d.drawRect(x - 5, gapY + gapSize/2, width + 10, 20);
    }
    
    private void drawGround(Graphics2D g2d) {
        int groundHeight = 50;
        g2d.setColor(GROUND_BROWN);
        g2d.fillRect(0, getHeight() - groundHeight, getWidth(), groundHeight);
        
        g2d.setColor(new Color(100, 60, 20));
        g2d.setStroke(new BasicStroke(3));
        g2d.drawLine(0, getHeight() - groundHeight, getWidth(), getHeight() - groundHeight);
    }
    
    private void drawScore(Graphics2D g2d, int score) {
        g2d.setColor(Color.WHITE);
        g2d.setFont(new Font("Arial", Font.BOLD, 48));
        String scoreStr = String.valueOf(score);
        FontMetrics fm = g2d.getFontMetrics();
        int x = (getWidth() - fm.stringWidth(scoreStr)) / 2;
        
        // Shadow
        g2d.setColor(Color.BLACK);
        g2d.drawString(scoreStr, x + 2, 52);
        
        // Score
        g2d.setColor(Color.WHITE);
        g2d.drawString(scoreStr, x, 50);
    }
    
    private void drawGameOver(Graphics2D g2d) {
        // Semi-transparent overlay
        g2d.setColor(new Color(0, 0, 0, 150));
        g2d.fillRect(0, 0, getWidth(), getHeight());
        
        // Game Over text
        g2d.setColor(Color.RED);
        g2d.setFont(new Font("Arial", Font.BOLD, 72));
        String msg = "GAME OVER";
        FontMetrics fm = g2d.getFontMetrics();
        int x = (getWidth() - fm.stringWidth(msg)) / 2;
        int y = getHeight() / 2;
        
        // Shadow
        g2d.setColor(Color.BLACK);
        g2d.drawString(msg, x + 3, y + 3);
        
        // Text
        g2d.setColor(Color.RED);
        g2d.drawString(msg, x, y);
    }
}

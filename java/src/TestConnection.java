import java.io.*;
import java.net.*;

/**
 * Simple test to verify Java can connect to Python server
 */
public class TestConnection {
    public static void main(String[] args) {
        System.out.println("Testing connection to Python server...");
        
        try {
            System.out.println("Attempting to connect to localhost:5000...");
            Socket socket = new Socket("localhost", 5000);
            System.out.println("SUCCESS: Connected to Python server!");
            
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            System.out.println("Reading data from server...");
            
            String line = in.readLine();
            if (line != null) {
                System.out.println("Received: " + line.substring(0, Math.min(100, line.length())));
            }
            
            socket.close();
            System.out.println("Connection test completed successfully!");
            
        } catch (IOException e) {
            System.err.println("ERROR: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

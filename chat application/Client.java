import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) throws Exception {
        System.out.println("Welcome to the chat client!");
        System.out.print("Enter server address: ");
        Scanner console = new Scanner(System.in);
        String serverAddress = console.nextLine();
        Socket socket = new Socket(serverAddress, 59001);
        Scanner in = new Scanner(socket.getInputStream());
        PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
        while (true) {
            String line = console.nextLine();
            if (line.toLowerCase().startsWith("/quit")) {
                break;
            }
            out.println(line);
            String response = in.nextLine();
            System.out.println(response);
        }
        socket.close();
    }
}
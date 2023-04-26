import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;

public class Server {

    private static ArrayList<PrintWriter> clients = new ArrayList<>();

    public static void main(String[] args) throws Exception {
        System.out.println("The chat server is running.");
        int clientNumber = 0;
        ServerSocket listener = new ServerSocket(59001);
        try {
            while (true) {
                new Handler(listener.accept(), clientNumber++).start();
            }
        } finally {
            listener.close();
        }
    }

    private static class Handler extends Thread {
        private String name;
        private Socket socket;
        private Scanner in;
        private PrintWriter out;

        public Handler(Socket socket, int clientNumber) {
            this.socket = socket;
            name = "Client " + clientNumber;
        }

        public void run() {
            try {
                in = new Scanner(socket.getInputStream());
                out = new PrintWriter(socket.getOutputStream(), true);

                clients.add(out);

                while (true) {
                    String input = in.nextLine();
                    if (input.toLowerCase().startsWith("/quit")) {
                        return;
                    }
                    for (PrintWriter client : clients) {
                        client.println(name + ": " + input);
                    }
                }
            } catch (Exception e) {
                System.out.println(e);
            } finally {
                clients.remove(out);
                try {
                    socket.close();
                } catch (IOException e) {
                }
            }
        }
    }
}
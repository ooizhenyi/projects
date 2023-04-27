import java.net.*;
import java.io.*;
import java.util.*;

public class Server {
    private static Vector<ClientHandler> clients = new Vector<>();

    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(1234);
        System.out.println("Server started on port 1234");

        while (true) {
            Socket socket = null;

            try {
                socket = serverSocket.accept();
                System.out.println("New client connected: " + socket);

                DataInputStream inputStream = new DataInputStream(socket.getInputStream());
                DataOutputStream outputStream = new DataOutputStream(socket.getOutputStream());

                System.out.println("Creating new user...");

                String username = inputStream.readUTF();
                String password = inputStream.readUTF();

                if (authenticateUser(username, password)) {
                    System.out.println("User authenticated: " + username);
                    ClientHandler client = new ClientHandler(socket, username, inputStream, outputStream);
                    Thread thread = new Thread(client);
                    clients.add(client);
                    thread.start();
                } else {
                    System.out.println("User authentication failed: " + username);
                    outputStream.writeUTF("Authentication failed");
                    socket.close();
                }

            } catch (Exception e) {
                socket.close();
                e.printStackTrace();
            }
        }
    }

    private static boolean authenticateUser(String username, String password) {
        // Implement your authentication mechanism here
        // For simplicity, we will just hardcode a single user
        return username.equals("user") && password.equals("password");
    }

    static class ClientHandler implements Runnable {
        private String name;
        final DataInputStream inputStream;
        final DataOutputStream outputStream;
        Socket socket;
        boolean isLoggedIn;

        public ClientHandler(Socket socket, String name, DataInputStream inputStream, DataOutputStream outputStream) {
            this.socket = socket;
            this.name = name;
            this.inputStream = inputStream;
            this.outputStream = outputStream;
            this.isLoggedIn = true;
        }

        @Override
        public void run() {
            String received;

            while (true) {
                try {
                    received = inputStream.readUTF();

                    if (received.equals("logout")) {
                        this.isLoggedIn = false;
                        this.socket.close();
                        break;
                    }

                    sendMessageToAllClients(received);

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            try {
                this.inputStream.close();
                this.outputStream.close();

            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        private void sendMessageToAllClients(String message) throws IOException {
            for (ClientHandler client : clients) {
                if (client.isLoggedIn) {
                    client.outputStream.writeUTF(this.name + ": " + message);
                }
            }
        }
    }
}

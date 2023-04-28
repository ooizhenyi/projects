// import java.io.*;
// import java.net.*;
// import java.util.Scanner;

// public class Client {
//     private static final int SERVER_PORT = 12345;
//     private static final String SERVER_ADDRESS = "localhost";

//     private static String username;
//     private static String password;

//     public static void main(String[] args) throws IOException {
//         Scanner scanner = new Scanner(System.in);

//         // Get username and password from user
//         System.out.print("Enter your username: ");
//         username = scanner.nextLine();
//         System.out.print("Enter your password: ");
//         password = scanner.nextLine();

//         // Create socket connection to server
//         Socket socket = new Socket(SERVER_ADDRESS, SERVER_PORT);

//         // Create input and output streams
//         ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());
//         ObjectInputStream in = new ObjectInputStream(socket.getInputStream());

//         // Send authentication information to server
//         out.writeObject(username);
//         out.writeObject(password);

//         // Wait for server response
//         boolean isAuthenticated;
//         try {
//             isAuthenticated = (boolean) in.readObject();
//             if (isAuthenticated) {
//                 System.out.println("Successfully authenticated as " + username);
    
//                 // Start sending and receiving messages
//                 new Thread(new ClientSender(out)).start();
//                 new Thread(new ClientReceiver(in)).start();
//             } else {
//                 System.out.println("Authentication failed. Please try again.");
//             }
//         } catch (ClassNotFoundException e) {
//             e.printStackTrace();
//         } 


//     }
// }

// class ClientSender implements Runnable {
//     private ObjectOutputStream out;

//     public ClientSender(ObjectOutputStream out) {
//         this.out = out;
//     }

//     public void run() {
//         Scanner scanner = new Scanner(System.in);

//         try {
//             while (true) {
//                 // Read user input and send message to server
//                 String message = scanner.nextLine();
//                 out.writeObject(message);
//             }
//         } catch (IOException e) {
//             e.printStackTrace();
//         }
//     }
// }

// class ClientReceiver implements Runnable {
//     private ObjectInputStream in;

//     public ClientReceiver(ObjectInputStream in) {
//         this.in = in;
//     }

//     public void run() {
//         try {
//             while (true) {
//                 // Read incoming messages from server and display to user
//                 String message = (String) in.readObject();
//                 System.out.println(message);
//             }
//         } catch (IOException | ClassNotFoundException e) {
//             e.printStackTrace();
//         }
//     }
// }


import java.io.*;
import java.net.*;

public class Client {
    private static Socket socket;
    private static DataInputStream inputStream;
    private static DataOutputStream outputStream;

    public static void main(String[] args) {
        try {
            socket = new Socket("localhost", 1234);
            System.out.println("Connected to server on port 1234");

            inputStream = new DataInputStream(socket.getInputStream());
            outputStream = new DataOutputStream(socket.getOutputStream());

            // Authentication
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            System.out.println("Enter your username:");
            String username = reader.readLine();
            System.out.println("Enter your password:");
            String password = reader.readLine();
            outputStream.writeUTF(username);
            outputStream.writeUTF(password);

            String message = "";
            while (!message.equals("logout")) {
                String received = inputStream.readUTF();
                System.out.println(received);

                System.out.print(username + ": ");
                message = reader.readLine();
                outputStream.writeUTF(message);
            }

            socket.close();
            inputStream.close();
            outputStream.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

# Reliable-Data-Transfer-
Developed in Visual Studio Code 2024
Author Brett Sullivan, Developed 3-1-24
Reliable Data Transfer (RDT) Program - Overview:

The Reliable Data Transfer (RDT) program facilitates the reliable transmission of data between a client and server by implementing a window-based protocol. Here's how it works:

Transmission within Window:

The program sends a set number of data packets, typically referred to as a window, with a default window size of 4 packets.
Waiting for Acknowledgment:

After sending each window of packets, the program waits for an acknowledgment (ack) from the server.
Handling Acknowledgments:

If no acknowledgment is received within a predefined number of iterations (or frames), the entire window of packets is resent to ensure reliable delivery.
In case the acknowledgment received does not match the expected acknowledgment, indicating potential packet loss or corruption, the entire window is resent to maintain data integrity.
Advancing the Window:

Upon receiving the expected acknowledgment, the program advances the window, allowing for the transmission of the next set of packets.
Handling Out-of-Order Packets:

To mitigate issues related to out-of-order or delayed packets, the program maintains a server data variable. Each received packet, along with its sequence number, is appended to this variable. This organization facilitates easy sorting at the end of transmission, ensuring that out-of-order and delayed packets are managed effectively.
In summary, the RDT program employs a window-based protocol to facilitate reliable data transfer between the client and server. By implementing strategies such as window-based transmission, acknowledgment handling, and server data organization, the program ensures the robustness and reliability of data transmission, even in challenging network conditions. 

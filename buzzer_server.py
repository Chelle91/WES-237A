import socket
import time

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Listen on all interfaces, port 12345
    server_socket.listen(1)
    print("Server listening on PC...")
    
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    
    while True:
        data = conn.recv(1024).decode()
        if not data or data == "DISCONNECT":
            break
        if data == "BEEP":
            print("Received BEEP command (Replace this with actual buzzer control if needed)")
            time.sleep(0.5)  # Simulating buzzer timing
    
    conn.close()
    server_socket.close()
    print("Server shut down.")

if __name__ == "__main__":
    server()

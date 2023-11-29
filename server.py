import socket
import telnetlib

# Impostazioni del server
HOST = '127.0.0.1'  # Indirizzo IP del server (vuoto per accettare connessioni su tutte le interfacce)
PORT = 23  # Porta su cui il server ascolterà

def handle_client(client):
    client.write(b"Benvenuto al server Telnet!\n")
    while True:
        command = client.read_until(b"\n")  # Leggi i dati inviati dal client fino al newline
        if command.strip().lower() == b"exit":
            client.write(b"Arrivederci!\n")
            break
        else:
            # Esegui l'elaborazione del comando qui
            response = b"Hai detto: " + command
            client.write(response + b"\n")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server Telnet in ascolto su {HOST} : {PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connessione accettata da {addr}")
            
            client = telnetlib.Telnet()
            client.sock = client_socket
            handle_client(client)
            client.close()

if __name__ == "__main__":
    run_server()

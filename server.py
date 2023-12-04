import socket
import telnetlib
import threading

HOST = '127.0.0.1'
PORT = 23
accounts = [
    {
        "nome": "admin",
        "psw": "admin",
    },
    {
        "nome": "franci",
        "psw": "admin",
    },
    {
        "nome": "mario",
        "psw": "admin",
    }
]

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.write(message)

def handle_client(client):
    clients.append(client)
    while True:
        try:
            # Fase di autenticazione
            client.write(b"Nome utente: ")
            username = client.read_until(b"\n").decode('ascii').strip()
            client.write(b"Password: ")
            password = client.read_until(b"\n").decode('ascii').strip()

            # Verifica delle credenziali
            for account in accounts:
                if account["nome"] == username and account["psw"] == password:
                    client.write(b"Accesso riuscito. Benvenuto nella chat!\n")
                    break
            else:
                client.write(b"Credenziali non valide. Accesso negato.\n")
                clients.remove(client)
                return

            # Fase di chat
            while True:
                message = client.read_until(b"\n")
                addr = client.get_socket().getpeername()
                message_with_addr = f"{username}: {message.decode('ascii')}".encode('ascii')
                broadcast(message_with_addr, client)
        except:
            clients.remove(client)
            break

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server Telnet in ascolto su {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connessione accettata da {addr}")
            
            client = telnetlib.Telnet()
            client.sock = client_socket
            
            client_thread = threading.Thread(target=handle_client, args=(client,))
            client_thread.start()

if __name__ == "__main__":
    run_server()
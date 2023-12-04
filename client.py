import telnetlib
import threading

# Impostazioni del client
HOST = '127.0.0.1'
PORT = 23

def read_from_server(client):
    while True:
        response = client.read_until(b"\n")
        print(response.decode('ascii'))

def run_client():
    with telnetlib.Telnet(HOST, PORT) as client:
        # Fase di autenticazione
        username = input("Nome utente: ")
        client.write((username + "\n").encode('ascii'))
        password = input("Password: ")
        client.write((password + "\n").encode('ascii'))

        # Attendi la risposta del server
        response = client.read_until(b"\n").decode('ascii').strip()
        print(response)

        # Se l'accesso non è riuscito, termina il client
        if "Accesso negato" in response:
            return

        # Avvia il thread di lettura solo dopo che la fase di registrazione è completata con successo
        read_thread = threading.Thread(target=read_from_server, args=(client,))
        read_thread.start()

        # Fase di chat
        while True:
            command = input()
            if command.strip().lower() == "exit":
                client.write((command + "\n").encode('ascii'))
                break
            else:
                client.write((command + "\n").encode('ascii'))

if __name__ == "__main__":
    run_client()
if __name__ == "__main__":
    run_client()
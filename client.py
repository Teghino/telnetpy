import telnetlib

# Impostazioni del client
HOST = '127.0.0.1'
PORT = 23

def run_client():
    with telnetlib.Telnet(HOST, PORT) as client:
        while True:
            command = input("Inserisci un comando: ")
            if command.strip().lower() == "exit":
                break
            else:
                client.write((command + "\n").encode('ascii'))
                response = client.read_until(b"\n")
                print("Risposta dal server:", response.decode('ascii'))

if __name__ == "__main__":
    run_client()
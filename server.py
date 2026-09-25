import socket
import threading
import ssl

def client_thread(client_socket, clients, usernames,address):
    print(f"\n[+] Estamos en client_thread")

    username = client_socket.recv(1024).decode()
    usernames[client_socket] = username

    print(f"\n[+] El usuario {username} se ha conectado al chat ")

    for client in clients:
        if client is not client_socket:
            client.sendall(f"\n[+] El usuario {username} ha entrado al chat \n\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if message == "/usuarios":
                client_socket.sendall(f"\n[+] Listado de usuarios disponibles: {', '.join(usernames.values())}\n\n".encode())
                continue
            
            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())
        except:
            break
    print(f"[!] El usuario {username} con ip {address} se ha desconectado")
    client_socket.close()
    clients.remove(client_socket)

    del usernames[client_socket]


def server_program():

    host = "localhost"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # TIME_WAIT
    server_socket.bind((host,port))

    #Configurar ssl antes de abrir la conexion a escucha
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server-cert.pem",keyfile="server-key.key")

    #Envolver el socket con ssl para que este cifrado
    server_socket = context.wrap_socket(server_socket, server_side=True)
    server_socket.listen()

    print(f"\n[+] El servidor está en escucha de conexiones entrantes...")

    clients = []
    usernames = {}

    while True:

        client_socket, address = server_socket.accept()
        clients.append(client_socket)

        print(f"\n[+] Se ha conectado un nuevo cliente: {address}")

        thread = threading.Thread(target=client_thread, args=(client_socket, clients, usernames,address))
        thread.daemon = True
        thread.start()

    server_socket.close()


if __name__ == "__main__":
    server_program()
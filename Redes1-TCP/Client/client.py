import socket
import os
 
def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
 
    while True:
        command = input("Digite o comando: ")
 
        if command == "exit":
            client_socket.send(command.encode())
            break
 
        client_socket.send(command.encode())
 
        if command.startswith("upload"):
            _, filename = command.split()
            if os.path.isfile(filename):
                with open(filename, 'rb') as f:
                    client_socket.sendfile(f)
            else:
                print("Arquivo não encontrado.")
                continue
 
        elif command.startswith("download"):
            response = client_socket.recv(4)
            if response == b'START':
                _, filename = command.split()
                with open(filename, 'wb') as f:
                    data = client_socket.recv(1024)
                    while data and data != b'END':
                        f.write(data)
                        data = client_socket.recv(1024)
                print(f"Arquivo '{filename}' baixado com sucesso.")
 
            else:
                print(response.decode())
 
        else:
            response = client_socket.recv(1024)
            print(response.decode())
 
    client_socket.close()
 
if __name__ == '__main__':
    client_program()
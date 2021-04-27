import socket
import threading

server = socket.socket()
server.bind(('0.0.0.0', 8000))
server.listen()

# block and wait for the client
sock, addr = server.accept()

BUFFER_SIZE = 1024
data = ""

while True:
    buff = sock.recv(BUFFER_SIZE).decode('uft8')
    if buff:
        data += buff
    else:
        break

print(data)
sock.close()


def handle_sock(sock, addr):
    data = ""
    while True:
        buff = sock.recv(BUFFER_SIZE)
        if buff:
            data += buff.decode('utf8')
        else:
            return data


while True:
    sock, addr = server.accept()
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()




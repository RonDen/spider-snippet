import socket
import threading

server = socket.socket()
server.bind(('0.0.0.0', 8000))
server.listen()

# block and wait for the client
# sock, addr = server.accept()

BUFFER_SIZE = 1024 * 10

def handle_sock(sock, addr):
    data = ""
    while True:
        buff = sock.recv(BUFFER_SIZE)
        data += buff.decode('utf8')
        print(data)
        request_template = """HTTP/1.1 200 OK

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>this is a simple page</h1>
</form>

</body>
</html>

        """
        sock.send(request_template.encode('utf8'))


if __name__ == '__main__':
    while True:
        # 阻塞等待连接
        sock, addr = server.accept()
        client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
        client_thread.setDaemon(True)
        client_thread.start()




import socket

client = socket.socket()
client.connect(('127.0.0.1', 8000))

client.send('bobby'.encode('utf-8'))
client.close()

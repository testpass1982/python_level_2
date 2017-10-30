from socket import *
import time
host = 'localhost'
port = 8000
s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print('server started and listening')
while True:
    client, addr = s.accept()
    print("connection found")
    presence = 'Hello from server'
    data = client.recv(1024).decode()
    print(data)
    r = 'Recieved: '+data
    client.send(r.encode())
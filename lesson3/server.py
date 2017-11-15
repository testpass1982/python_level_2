from socket import *
import json

class Connect(object):
    def __init__(self):
        try:
            self.s = socket(AF_INET, SOCK_STREAM)
        except:
            print('socket cannot be created')
        server_address = ('localhost', 7777)
        self.s.bind(server_address)
        self.s.listen(5)
        self.connections = []

    def listen(self):
        while True:
            connection, client_address = self.s.accept()
            self.connections.append(connection)
            print('Client connected')
            try:
                data = connection.recv(1024).decode()
                data = json.loads(data)
                print(data)
            finally:
                connection.close()

def main():
    connect = Connect()
    connect.listen()

if __name__ == '__main__':
    main()
from socket import *

class Connect(object):
    def __init__(self):
        try:
            self.s = socket(AF_INET, SOCK_STREAM)
        except:
            print('socket cannot be created')
        server_address = ('localhost', 7777)
        self.s.bind(server_address)
        self.s.listen(5)

    def listen(self):
        while True:
            connection, client_address = self.s.accept()
            print('Client connected')
            try:
                data = connection.recv(16).decode()
                print(data)
                r = 'Recieved: ' + data
                connection.send(r.encode())
            finally:
                connection.close()

def main():
    connect = Connect()
    connect.listen()

if __name__ == '__main__':
    main()
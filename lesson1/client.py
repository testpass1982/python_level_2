from socket import *

class Client(object):
    def __init__(self):
        try:
            self.host = 'localhost'
            self.port = 7777
            self.data = ''
            self.create_socket(self.host, self.port)
        except:
            print('There was a problem')

    def create_socket(self, addr, port):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((addr, port))


    def send_message(self, message):
        self.s.send(message.encode())
        self.data = self.s.recv(1024).decode()
        self.s.close()

# def send_input(message):
#     s = socket(AF_INET, SOCK_STREAM)
#     host = 'localhost'
#     port = 7777
#     s.connect((host, port))
#     s.send(message.encode())
#     data = s.recv(1024).decode()
#     print(data)
#     s.close()

def main():
    client = Client()
    r = input("Please, enter a message: ")
    while r != 'exit':
        client.send_message(r)
        print(client.data)

if __name__ == '__main__':
    main()
from socket import *
import codes
import json
import struct

users = {
    'Anatoliy': 'password',
    'Popov': 'testpass',
    'Ivanov': 'ivanov_password'
}

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
                data = connection.recv(1024).decode()
                data = json.loads(data)
                print(data)
                if data['action'] == 'presence':
                    connection.send(codes.OK.encode())
                if data['action'] == 'authenticate':
                    if data['user']['account_name'] in users:
                        connection.send(codes.ACCEPTED.encode())
                    else:
                        connection.send(codes.WRONG_LOGIN_OR_PASSWORD.encode())
            finally:
                connection.close()

    def prefix_len(self, msg):
        msg = struct.pack('>I', len(msg)) + bytes(msg, 'utf-8')
        return msg

def main():
    connect = Connect()
    connect.listen()

if __name__ == '__main__':
    main()
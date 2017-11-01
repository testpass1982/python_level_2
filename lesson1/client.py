import socket
import sys
import time
import user
import json
import struct

host = 'localhost'
port = 7777


class Client():
    def __init__(self, host, port, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.host = host
        self.port = port

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        self.connect(self.host, self.port)
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket conneciton broken")
            totalsent = totalsent + sent

    def receive(self):
        # chunks = []
        # bytes_recieved = 0
        # while bytes_recieved < len(self.msg):
        #     chunk = self.sock.recv(min(len(self.msg) - bytes_recieved, 1024))
        #     if chunk == b'':
        #         raise RuntimeError("socket connection broken")
        #     chunks.append(chunk)
        #     bytes_recieved = bytes_recieved + len(chunk)
        # return b''.join(chunks)

        raw_msglen = self.recvall(self.sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvall(self.sock, msglen)

    def send_presence(self):
        presence_message = {
            "action": "presence",
            "time": time.ctime(),
            "user": {
                "account_name": user.account_name,
                "status": user.status
            }
        }
        self.send(json.dumps(presence_message).encode('utf-8'))
        status = self.sock.recv(1024).decode()
        print(status)

    def login(self):
        login_data = {
            "action": "authenticate",
            "time": time.ctime(),
            "user": {
                "account_name": user.account_name,
                "password": user.password
            }
        }
        self.send(json.dumps(login_data).encode('utf-8'))
        status = self.sock.recv(1024).decode()
        print(status)

    def recvall(self, sock, n):
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
        return data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
        port = int(sys.argv[2])
    client = Client(host, port)
    client.login()
    client.send_presence()

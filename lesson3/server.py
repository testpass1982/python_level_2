import sys
from socket import *
import json
import select
import logging
from useful.configuration import *
from useful.protocol import JMessage

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = self._start()
        self._clients = []

    def _start(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(15)
        s.settimeout(0.2)
        return s

    def _listen(self):
        try:
            connection, address = self.socket.accept()
            presense_msg_bytes = connection.recv(1024)
            presense_msg = JMessage.create_from_bytes(presense_msg_bytes)
            if presence_msg.action == PRESENSE:
                presence_response = JResponse(**{RESPONSE: OK})
                connection.send(bytes(presence_response))

    def server_loop():
        while True:
            self._listen()

if __name__ == '__main__':
    print('Запуск сервера')
    # Получаем аргументы скрипта
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    app = Server(addr, port)
    app.server_loop()
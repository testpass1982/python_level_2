import random
import datetime
import time
import sys
from useful.protocol import JMessage
from socket import socket, AF_INET, SOCK_STREAM
from tkinter import *
from useful.configuration import *
import threading

host = 'localhost'
port = 7777

class App(Frame):
    version = "0.1"

    def __init__(self, master, host='localhost', port=7777):
        super(App, self).__init__(master)
        self.server = host
        self.port = port
        self.name = 'Anatoly'
        self.socket = self._connect()
        self.disconnected = False
        # print("Enter your name: ", end = "")
        # while not self.name:
        #     self.name = input().strip()
        #     if " " in self.name:
        #         print("Your name cannot contain spaces: ", end = "")
        # if not self.name:
        #     self.name = "Anonymous" + str(random.randrange(1, 1000))
        self.grid()
        self.data_buff = 4096
        # self.sent_messages = []
        self.create_widgets()
        t1 = threading.Thread(target=self.get_messages)
        t1.start()

    def _connect(self):
        print("Попытка подключения к ", self.server, "по порту", self.port)
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.server, self.port))
            print("Connection established.")
            return s
        except Exception as e:
            print(e)

    def send_recieve_loop(self):
        nick_msg = JMessage(action=PRESENCE, time=time.time(), nickname=
        self.name)
        self.socket.send(nick_msg)

    def create_widgets(self):
        self.nickname_lbl = Label(self, text = "Nickname: " + self.name)
        self.nickname_lbl.grid(row = 0, column = 0, sticky = N)
        self.message_output = Text(self, width = 80, height = 40, wrap = WORD)
        self.message_output.grid(row = 1, column = 0, columnspan=2)
        self.message_input = Entry(self, width=100)
        self.message_input.grid(row = 2, column = 0, sticky = W+S+E+N)
        self.submit_btn = Button(self, text = "Send", command =
        self.submit_message)
        self.submit_btn.grid(row = 2, column = 1, sticky = E)

    def submit_message(self):
        input_text = self.message_input.get().strip()
        input_text_sending = JMessage(action=MSG, time=time.ctime(),
                                      nickname=self.name, text=input_text)
        if not input_text:
            self.message_input.delete(0, END)
            return
        try:
            self.socket.send(bytes(input_text_sending))
            self.message_input.delete(0, END)
            self.insert_message_to_chat(input_text)
        except Exception as e:
            print(e)

    def insert_message_to_chat(self, message):
        global log
        log = self.message_output.get("1.0", END).strip()
        if not log:
            log = self.name+': '+message.strip()
        else:
            log = log + '\n' + self.name +': '+message
        self.message_output.config(state=NORMAL)
        self.message_output.delete("1.0", END)
        self.message_output.insert("1.0", log)
        self.message_output.config(state=DISABLED)
        self.message_output.yview("moveto", 1)

    def get_messages(self):
        while True:
            if self.disconnected:
                break
            data = self.socket.recv(self.data_buff)
            if not data:
                break
            decoded = data.decode("utf-8")
            self.insert_message(decoded)
        # s.close()
        # time = datetime.datetime.now().strftime('%H:%M:%S')
        # self.insert_message("[{}] disconnected.".format(time))

    def disconnect(self):
        if not self.disconnected:
            self.disconnected = True
            self.socket.close()
            time = datetime.datetime.now().strftime('%H:%M:%S')
            disconnect_message = "[{}] Disconnected.".format(time)
            print(disconnect_message)
            self.insert_message_to_chat(disconnect_message)

if __name__ == '__main__':
    try:
        host = sys.argv[1]
    except IndexError:
        host = 'localhost'
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print("Port must be an integer")
        sys.exit(0)

    root = Tk()
    app = App(root, host, port)
    root.title("Messenger V{}.".format(str(App.version)))
    root.mainloop()
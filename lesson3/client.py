import socket
import random
import datetime
import time
import sys

from tkinter import *

host = 'localhost'
port = 7777

class App(Frame):
    version = "0.1"

    def __init__(self, master, host, port):
        super(App, self).__init__(master)
        self.server = host
        self.port = port
        self.name = ''
        print("Enter your name: ", end = "")
        while not self.name:
            self.name = input().strip()
            if " " in self.name:
                print("Your name cannot contain spaces: ", end = "")
        if not self.name:
            self.name = "Anonymous" + str(random.randrange(1, 1000))
        self.grid()
        self.data_buff = 4096
        self.sent_messages = []
        self.create_widgets()
        nick_msg = "Nickname {}".format(self.name)

        s.send(nick_msg.encode())

    def connect(self):
        print("Попытка подключения к ", self.server, "по порту", self.port)
        try:
            s.connect((self.server, self.port))
            print("Connection established.")
            return True
        except Exception as e:
            print(e)
            return False

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
        message = self.message_input.get().strip()
        if not message:
            self.message_input.delete(0, END)
            return
        data = message.encode()
        s.send(data)
        self.message_input.delete(0, END)

    def insert_message(self, message):
        global log
        log = self.message_output.get("1.0", END).strip()
        if not log:
            log = message.strip()
        else:
            log = log + '\n' + message
        self.message_output.config(state=NORMAL)
        self.message_output.delete("1.0", END)
        self.message_output.insert("1.0", log)
        self.message_output.config(state=DISABLED)
        self.message_output.yview("moveto", 1)

    def get_messages(self):
        while True:
            if self.disconnected:
                break
            data = s.recv(self.data_buff)
            if not data:
                break
            decoded = data.decode("utf-8")
            self.insert_message(decoded)
        s.close()
        time = datetime.datetime.now().strftime('%H:%M:%S')
        self.insert_message("[{}] disconnected.".format(time))

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

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    root = Tk()
    app = App(root, host, port)
    root.title("Messenger V{}.".format(str(App.version)))
    root.mainloop()
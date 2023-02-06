import socket
import config
import threading
import datetime


class Client:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.FORMAT = 'utf-8'

        self.client = socket.socket()
        self.client.connect((self.HOST, self.PORT))

    def receive(self):
        while True:
            data = self.client.recv(1024)
            if data:
                print(data.decode(self.FORMAT))

    def send(self):
        while True:
            data = input("Write City\n").capitalize().encode(self.FORMAT)
            self.client.send(data)

    def run(self):
        rcv_thread = threading.Thread(target=self.receive)
        send_thread = threading.Thread(target=self.send)
        rcv_thread.start()
        send_thread.start()


Client(config.HOST, config.PORT).run()

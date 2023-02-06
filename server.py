import socket
import config
import threading
import datetime
import requests
import json


class Server:
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.FORMAT = 'utf-8'

        self.server = socket.socket()
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()

    def __get_weather(self, data):
        response = requests.get(
            f'http://api.weatherapi.com/v1/current.json?key={config.API_WEATHER_KEY}&q={data.decode(self.FORMAT)}').json()
        print(response)
        return f"City: {response['location']['name']}\n" \
               f"Country: {response['location']['country']}\n" \
               f"Condition: {response['current']['condition']['text']}\n" \
               f"Temp: {response['current']['temp_c']}\n".encode(self.FORMAT)

    def __receive(self, client):
        while True:
            try:
                data = client.recv(1024)
                client.send(self.__get_weather(data))
            except Exception as e:
                print(e)

    def run(self):
        print('[SERVER IS WORKING]')
        print(f"[{datetime.datetime.now()}]")
        while True:
            client, addr = self.server.accept()
            print(f"[NEW CONNECTION] {addr}")

            receive_thread = threading.Thread(target=self.__receive(client))
            receive_thread.start()


Server(config.HOST, config.PORT).run()

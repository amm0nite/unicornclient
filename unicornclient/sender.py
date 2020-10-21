import queue
import threading
import logging

class Sender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue.Queue()
        self.client = None
        self.mqtt_client = None

    def set_client(self, client):
        self.client = client

    def set_mqtt_client(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def send(self, message):
        self.queue.put(message)

    def run(self):
        while True:
            message = self.queue.get()
            self.send_one(message)
            self.queue.task_done()

    def send_one(self, message):
        if not self.client.socket:
            return

        try:
            self.client.socket.sendall(message.encode())
        except OSError as err:
            logging.error('sender error')
            logging.error(err)
            self.client.socket = None

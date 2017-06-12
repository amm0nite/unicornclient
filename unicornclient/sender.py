
import threading

class Sender(object):
    def __init__(self):
        self.socket = None
        self.lock = threading.Lock()

    def send(self, message):
        if not self.socket:
            return

        with self.lock:
            self.socket.sendall(message.encode())

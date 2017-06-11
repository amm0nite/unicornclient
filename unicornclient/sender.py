import json
import threading

class Sender(object):
    def __init__(self):
        self.socket = None
        self.lock = threading.Lock()

    def send(self, reply, stream=None):
        if not self.socket:
            return

        header = json.dumps(_clean_dict(reply))
        header_size = len(header.encode())
        body = b''
        body_size = 0

        if stream:
            body = stream.read()
            body_size = len(body)

        message_start = str(header_size) + ',' + str(body_size) + ':'
        message = message_start.encode() + header.encode()
        if body_size > 0:
            message += body

        with self.lock:
            self.socket.sendall(message)


def _clean_dict(data):
    if not isinstance(data, dict):
        return data

    new_dict = {}
    for key in data.keys():
        value = data[key]
        if value is not None:
            new_dict[key] = _clean_dict(value)

    return new_dict

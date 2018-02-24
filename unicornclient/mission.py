
import json

from . import message

class Mission(object):
    def __init__(self, sender):
        self.sender = sender

    def send(self, message):
        self.sender.send(message)

    def post(self, name, data):
        msg = message.Message({ 'type': 'mission', 'name': name })
        if isinstance(data, dict):
            msg.set_body(json.dumps(data).encode())
        else:
            msg.set_body(data)
        self.sender.send(msg)

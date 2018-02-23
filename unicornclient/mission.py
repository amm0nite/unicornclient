
class Mission(object):
    def __init__(self, sender):
        self.sender = sender

    def send(self, message):
        self.sender.send(message)
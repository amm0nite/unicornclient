
import logging

from . import sender
from . import manager
from . import client
from . import config
from . import mqtt_client

class Agent():
    def __init__(self):
        logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)

    def main(self):
        _sender = sender.Sender()
        _manager = manager.Manager(_sender)
        _manager.start_default()

        _sender.daemon = True
        _sender.start()

        _client = client.Client(_manager, _sender)
        _client.start()

        _mqtt_client = mqtt_client.MQTTClient()
        _mqtt_client.start()


if __name__ == '__main__':
    agent = Agent()
    agent.main()

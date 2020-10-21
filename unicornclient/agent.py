
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
        _manager = manager.Manager()
        _client = client.Client()
        _mqtt_client = mqtt_client.MQTTClient()

        _client.set_manager(_manager)
        _mqtt_client.set_manager(_manager)

        _sender.set_client(_client)
        _sender.set_mqtt_client(_mqtt_client)
        _manager.set_sender(_sender)

        _sender.start()
        _client.start()
        _mqtt_client.start()
        _manager.start_default()


if __name__ == '__main__':
    agent = Agent()
    agent.main()

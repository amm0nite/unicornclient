import time
import logging
import threading
import paho.mqtt.client as mqtt

from . import config

MQTT_KEEP_ALIVE = 60

class MQTTClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.manager = None
        self.client = None
        self.backoff = 1

    def set_manager(self, manager):
        self.manager = manager

    def run(self):
        if not config.MQTT_HOST:
            return

        while True:
            try:
                logging.info('MQTT Connecting')
                self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
                self.client.on_connect = self.on_connect
                self.client.on_message = self.on_message

                self.client.connect(config.MQTT_HOST, config.MQTT_PORT, MQTT_KEEP_ALIVE)
                self.client.loop_forever(retry_first_connection=True)
            except OSError as err:
                self.client.disconnect()
                logging.info('MQTT error')
                logging.error(err)

            self.backoff *= 2
            logging.info('MQTT Retry in %ds', self.backoff)
            time.sleep(self.backoff)

    def on_connect(self, client, userdata, flags, rc):
        # pylint: disable=unused-argument
        logging.info('MQTT Connected with result code %s', str(rc))
        self.backoff = 1
        #client.subscribe("$SYS/#")

    def on_message(self, client, userdata, msg):
        # pylint: disable=unused-argument
        logging.debug("%s %s", msg.topic, str(msg.payload))

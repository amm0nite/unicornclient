
import logging
import threading
import paho.mqtt.client as mqtt

from . import config

MQTT_KEEP_ALIVE = 60

class MQTTClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(config.MQTT_HOST, config.MQTT_PORT, MQTT_KEEP_ALIVE)
        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        logging.info("MQTT Connected with result code "+str(rc))
        #client.subscribe("$SYS/#")

    def on_message(self, client, userdata, msg):
        logging.debug(msg.topic+" "+str(msg.payload))
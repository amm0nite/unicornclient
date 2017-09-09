import threading
import logging
import queue

from .. import message

try:
    from yoctopuce.yocto_api import YAPI
    from yoctopuce.yocto_temperature import YTemperature
except ImportError:
    YAPI, YTemperature = None, None
    logging.warning("No yoctopuce module")

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.manager = None
        self.channel1 = None
        self.channel2 = None

    def run(self):
        self.setup_channels()

        while True:
            self.queue.get()

            temps = self.get_temperatures()
            if temps:
                text = str(temps[0])[:3] + str(temps[1])[:3]
                payload = {
                    'type':'status',
                    'status': {
                        'temp1' : temps[0],
                        'temp2' : temps[1],
                    }
                }

                self.manager.forward('dothat', {'text': text})
                self.manager.send(message.Message(payload))

            self.queue.task_done()

    def setup_channels(self):
        if not YAPI or not YTemperature:
            raise Exception('no module')

        YAPI.RegisterHub("usb")
        sensor = YTemperature.FirstTemperature()

        if sensor is None:
            raise Exception('no sensor')
        if not (sensor.isOnline()):
            raise Exception('sensor offline')

        serial = sensor.get_module().get_serialNumber()
        self.channel1 = YTemperature.FindTemperature(serial + '.temperature1')
        self.channel2 = YTemperature.FindTemperature(serial + '.temperature2')

    def get_temperatures(self):
        if self.channel1.isOnline() and self.channel2.isOnline():
            temp1 = self.channel1.get_currentValue()
            temp2 = self.channel2.get_currentValue()
            return (temp1, temp2)

        return None

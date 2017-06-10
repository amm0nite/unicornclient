import socket
import time
import random

from . import config
from . import parser
from . import handler
from . import sender
from . import manager

TIMEOUT = 30

class ShutdownException(Exception):
    pass

def main():
    _parser = parser.Parser()
    _sender = sender.Sender()

    _manager = manager.Manager(_sender)
    _handler = handler.Handler(_manager)
    _manager.start()

    while True:
        client = None
        try:
            address = (config.HOST, config.PORT)
            print('connecting to ' + str(address))
            client = socket.create_connection(address, TIMEOUT)
            client.settimeout(TIMEOUT)
            print('connected')

            _sender.socket = client
            _manager.authenticate()

            while True:
                data = client.recv(128)
                if not data:
                    raise ShutdownException()
                payload = _parser.parse(data)
                if not payload:
                    continue
                _handler.handle(payload)

        except socket.error as err:
            print('socket error')
            print(err)
        except ShutdownException as err:
            print('server shutdown')
        finally:
            if client:
                client.close()

        time.sleep(random.randint(0, 9))

if __name__ == '__main__':
    main()

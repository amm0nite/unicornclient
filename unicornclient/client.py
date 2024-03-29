# pylint: disable=too-many-branches

import socket
import time
import logging
import ssl
import datetime
import subprocess
import threading

from . import config
from . import parser
from . import handler

CONNECTION_TIMEOUT = 30
REBOOT_TIMEOUT = 6

class ShutdownException(Exception):
    pass

class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = None
        self.manager = None
        self.backoff = 1

    def set_manager(self, manager):
        self.manager = manager

    def run(self):
        start = datetime.datetime.now()

        _parser = parser.Parser()
        _handler = handler.Handler(self.manager)

        while True:
            client = None
            try:
                address = (config.HOST, config.PORT)
                logging.info('client connecting to %s (secure: %s)', address, config.SSL_VERIFY)

                connection = socket.create_connection(address, CONNECTION_TIMEOUT)
                connection.settimeout(CONNECTION_TIMEOUT)

                ssl_context = ssl.create_default_context()
                if not config.SSL_VERIFY:
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                client = ssl_context.wrap_socket(connection, server_hostname=address[0])

                logging.info('client authenticating')
                self.socket = client
                self.manager.authenticate()
                self.backoff = 1

                while True:
                    start = datetime.datetime.now()
                    data = client.recv(128)
                    if not data:
                        raise ShutdownException()
                    _parser.feed(data)
                    parsed = _parser.parse()
                    for message in parsed:
                        _handler.handle(message)
                    if not self.socket:
                        raise ShutdownException()

            except socket.error as err:
                logging.error('client socket error')
                logging.error(err)
            except ShutdownException:
                logging.critical('server shutdown')
            finally:
                if client:
                    client.close()

            restarting = False
            elapsed = datetime.datetime.now() - start
            if elapsed > datetime.timedelta(hours=REBOOT_TIMEOUT):
                restarting = self.reboot()
            if not restarting:
                self.backoff *= 2
                logging.info('client retrying in %ds', self.backoff)
                time.sleep(self.backoff)
            else:
                return

    def reboot(self):
        return subprocess.call('reboot', shell=True) == 0

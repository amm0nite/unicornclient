# pylint: disable=W0122

import os
import logging

from . import config
from . import routine

class Manager(object):
    def __init__(self, sender):
        logging.info('creating manager')
        self.sender = sender
        self.threads = {}

    def start_default(self):
        self.start_routines(config.DEFAULT_ROUTINES)

    def start_routines(self, routines):
        for routine_name in routines:
            if not routine_name in self.threads:
                self.start_routine(routine_name)

    def start_routine(self, name, code=None):
        if name in self.threads:
            logging.warning("routine " + str(name) + " already started")
            return

        if not code:
            code = self.__find_code(name)

        if not code:
            raise Exception('no code for ' + name)

        logging.info("starting routine " + str(name))
        context = {}
        exec(code, context)

        user_routine_class = self.__find_subclass(context)
        if not user_routine_class:
            raise Exception('no routine subclass defined in code for ' + name)

        user_routine = user_routine_class()
        user_routine.manager = self
        user_routine.daemon = True
        user_routine.start()
        self.threads[name] = user_routine

    def __find_code(self, name):
        routine_path = os.path.join(os.path.dirname(__file__), 'routines', name + '.py')
        try:
            with open(routine_path, 'r') as routine_file:
                return routine_file.read()
        except FileNotFoundError as err:
            logging.error(err)
            return None

    def __find_subclass(self, context):
        for key in context:
            try:
                if issubclass(context[key], routine.Routine):
                    return context[key]
            except TypeError:
                pass
        return None

    def join(self):
        for thread in self.threads.values():
            thread.join()

    def forward(self, name, task):
        if name == 'routine' and 'name' in task:
            code = task['code'] if 'code' in task else None
            self.start_routine(name, code)
            return

        if name in self.threads:
            self.threads[name].queue.put(task)
            return

    def send(self, message):
        self.sender.send(message)

    def authenticate(self):
        self.forward('auth', {'action':'authenticate'})

import threading
import queue

class Routine(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue.Queue()
        self.manager = None
        self.no_wait = False

    def run(self):
        while True:
            data = None

            if self.no_wait:
                data = self.queue.get_nowait()
            else:
                data = self.queue.get()

            if data:
                index = 'routine_command'
                routine_command = data[index] if index in data else None

                if routine_command == 'stop':
                    return

            self.process(data)
            self.queue.task_done()

    def process(self, data):
        pass

from unicornclient import routine

class Routine(routine.Routine):
    def __init__(self):
        routine.Routine.__init__(self)

    def process(self, data):
        self.mission.send_skills()

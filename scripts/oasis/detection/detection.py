from .monitor import MonitorConnection
from .jamming import JammingModule



class Detector(object):

    def __init__(self, target, modules=[]):

        self.modules = {
                'monitor': None,
                'jamming': None,
                'btlejack': None,
                'injectable': None,
        }

        if 'monitor' in modules:
            self.modules['monitor'] = MonitorConnection()

        if 'jamming' in modules:
            self.modules['jamming'] = JammingModule()

        '''
        if 'btlejack' in modules:
            self.modules['btlejack'] = BTLEJack()

        if 'injectable' in modules:
            self.modules['injectable'] = Injectable()
        '''


    def detect(self, message):

        metrics = message

        # Note: what should be returned ? True / False ? raise an exception ? how to "alert" when an attack is detected ?
        for module in self.modules.values():
            if module != None:
                mtc = metrics
                module.detect(mtc)



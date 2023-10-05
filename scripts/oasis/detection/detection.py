from enum import IntEnum

from . import MonitorConnection



class ALERT(IntEnum):
    OTHER = 0
    BTLEJACK = 1
    BTLEJUICE = 2
    GATTACKER = 3
    INJECTABLE = 4
    JAMMING = 5
    KNOB = 6



class Module(object):
    
    def __init__(self):
        self.callbacks = {
                0x0 : self.time_callback,
                0x1 : self.scan_callback, 
                0x2 : self.conn_init_callback, 
                0x3 : self.conn_delete_callback, 
                0x4 : self.conn_rx_callback, 
                0x5 : self.conn_tx_callback, 
        }

    def alert(self, alert, metrics):
        access_addr = metrics['current_connection']['access_address']
        channel_no = metrics['current_connection']['channel_map']
        print(f">ALERT< {alert}: Access Address: {access_address}, Channel Number: {channel_no}")

    def detect(self, metrics):
        opcode = metrics['opcode_metric']
        cb = self.callbacks.get(opcode, None)
        if cb is not None:
            cb(metrics)


    def time_callback(self, metrics):
        pass

    def scan_callback(self, metrics):
        pass

    def conn_init_callback(self, metrics):
        pass

    def conn_delete_callback(self, metrics):
        pass

    def conn_rx_callback(self, metrics):
        pass

    def conn_tx_callback(self, metrics):
        pass



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
        for module in self.modules:
            mtc = metrics
            module.detect(mtc)



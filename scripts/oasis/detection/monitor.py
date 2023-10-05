from enum import IntEnum

from .detection import ALERT, Module





class MonitorConnection(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(target, *args, **kwargs)


    def conn_rx_callback(self, metrics):
        self.alert(ALERT.OTHER, metrics)

    def conn_tx_callback(self, metrics):
        self.alert(ALERT.OTHER, metrics)


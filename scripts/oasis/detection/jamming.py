from .module import ALERT, Module



class JammingModule(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(target, *args, **kwargs)


    def conn_rx_callback(self, metrics):
        pass

    def conn_tx_callback(self, metrics):
        pass


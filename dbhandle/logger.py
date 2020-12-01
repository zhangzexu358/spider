import logging
import sys

class StdOut(logging.Logger):
    def __init__(self, application):
        super(StdOut, self).__init__(application, logging.DEBUG)
        fmt = '%(asctime)s %(levelname)s: %(message)s'
        hdlr = logging.StreamHandler(sys.stdout)
        hdlr.formatter = logging.Formatter(fmt)
        self.addHandler(hdlr)
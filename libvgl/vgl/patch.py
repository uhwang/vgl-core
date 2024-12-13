'''
patch.py
'''

from . import basicshape
from . import vaxis

class Patch():
    def __init__(self, frm):
        self.frm = frm
        self.circle_list = []
        self.arrow_list = []
    
    def add_vaxis2d(self, sx, sy, xlen=1, ylen=1):
        ar = vaxis.VAxis2D(self.frm, sx, sy, xlen, ylen)
        self.arrow_list.append(ar)
        return ar
        
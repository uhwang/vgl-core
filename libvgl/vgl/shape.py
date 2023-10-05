'''
    shape.py
'''
from . import vertex
from . import linepat
from . import linetype

class Shape(vertex.Vertex, linetype.LineLevelC):
    def __init__(   self, 
                    sx, sy, 
                    nvert, 
                    edge, 
                    lcol, 
                    lthk,
                    fcol=None, 
                    lpat = linepat._PAT_SOLID,
                    pat_len=0.04
                ):
        vertex.Vertex.__init__(self, nvert=nvert)
        linetype.LineLevelC.__init__(self, lcol=lcol, lthk=lthk, lpat=lpat, pat_len=pat_len)
        self.sx = sx
        self.sy = sy
        self.edge = edge
        self.fcol = fcol
    
    def set_fcol(self, col): self.fcol = col
    def set_lcol(self, col): self.lcol = col
    def set_fill(self, mode): self.fill = mode

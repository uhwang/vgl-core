'''
    vaxis.py

    12/11/2024
    
'''
import math

from . import basicshape
from . import color
from . import util
from . import linepat


class VAxis2D():
    def __init__(self, 
                 frm,
                 sx        = 0, 
                 sy        = 0, 
                 xlen      = 1, 
                 ylen      = 1,
                 angle     = 0,  # degree
                 rad       = False,
                 # X-Axis 
                 xlcol     = color.RED,
                 xlthk     = 0.005,
                 xlpat     = linepat._PAT_SOLID,
                 xpat_len  = 0.04,
                 xacol     = color.RED,
                 xatype_t  = basicshape._ARROW_HEAD_TYPE_CLOSEDBLANK, 
                 xaangle   = basicshape._ARROW_HEAD_ANGLE, 
                 xalength  = basicshape._ARROW_HEAD_LENGTH_1,
                 # Y-Axis
                 ylcol     = color.GREEN,
                 ylthk     = 0.005,
                 ylpat     = linepat._PAT_SOLID,
                 ypat_len  = 0.04,
                 yacol     = color.GREEN,
                 yatype_t  = basicshape._ARROW_HEAD_TYPE_CLOSEDBLANK, 
                 yaangle   = basicshape._ARROW_HEAD_ANGLE, 
                 yalength  = basicshape._ARROW_HEAD_LENGTH_1,
                ):
        
        self.sx, self.sy = sx,sy
        
        if float(angle) != 0.0:
            rp = xlen*util.rad_rotation(xlen,0,angle) if rad else\
                 xlen*util.deg_rotation(xlen,0,angle)
            xex, xey = sx+rp[0], sy+rp[1]
            yex, yey = sx-rp[1], sy+rp[0]
        else:
            xex, xey = sx+xlen, sy 
            yex, yey = sx, sy+ylen           

        self.xaxis = basicshape.EndArrowLine(frm, sx, sy, xex, xey, xlcol, xlthk, xlpat, 
                                             xpat_len, True, xacol, xatype_t, xaangle, xalength)
        self.yaxis = basicshape.EndArrowLine(frm, sx, sy, yex, yey, ylcol, ylthk, ylpat, 
                                             ypat_len, True, yacol, yatype_t, yaangle, yalength)

    def rotate(self, angle, rad=False):
        self.xaxis.rotate(angle, rad)
        self.yaxis.rotate(angle, rad)
        self.sx = self.xaxis.sx
        self.sy = self.xaxis.sy    
        
    # rotate about self.sx, self.sy
    def rotate_s(self, angle, rad=False):
        self.xaxis.rotatep(self.sx, self.sy, angle, rad)
        self.yaxis.rotatep(self.sx, self.sy, angle, rad)
        self.sx = self.xaxis.sx
        self.sy = self.xaxis.sy
        
    def rotate_p(self, px, py, angle, rad=False):
        self.xaxis.rotatep(px, py, angle, rad)
        self.yaxis.rotatep(px, py, angle, rad)
        self.sx = self.xaxis.sx
        self.sy = self.xaxis.sy
                
    def translate(self, x, y):
        self.sx, self.sy = x,y
        self.xaxis.translate(x,y)
        self.yaxis.translate(x,y)

    def translate_r(self, dx, dy):
        self.sx = self.sx+dx
        self.sy = self.sy+dy
        self.xaxis.rtranslate(dx,dy)
        self.yaxis.rtranslate(dx,dy)

    def draw(self, dev):
        self.xaxis.draw(dev)
        self.yaxis.draw(dev)
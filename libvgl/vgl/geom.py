# Vector Graphic Library (VGL) for Python
#
# geom.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#

import numpy as np
from . import color, rotation, vertex
from . import linetype
from . import shape
from . import linepat
from . import shape
from . import util

#def distP(x1,y1,x2,y2): return np.sqrt((x2-x1)**2+(y2-y1)**2)
#def distV(vlist): return np.sqrt( (vlist[2]-vlist[0])**2+(vlist[3]-vlist[1])**2 )

SQUARE_MODE_NEW = -1
SQUARE_MODE_CENTER = 0
SQUARE_MODE_LEFTTOP = 1
SQUARE_MODE_RIGHTTOP = 2
SQUARE_MODE_LEFTBOTTOM = 3 
SQUARE_MODE_RIGHTBOTTOM = 4

class Square(shape.Shape):
    def __init__(self,x,y,edge,lcol=color.BLACK, lthk=0.001,fcol=None, 
        mode=SQUARE_MODE_CENTER):
        super().__init__(x,y,4,edge,lcol,lthk,fcol,fill)
        self.mode = mode
    
        if   mode == SQUARE_MODE_CENTER:
            self.center()
        elif mode == SQUARE_MODE_LEFTTOP:
            self.leftop()
        elif mode == SQUARE_MODE_RIGHTTOP:
            self.righttop()
        elif mode == SQUARE_MODE_LEFTBOTTOM :
            self.leftbottom()
        elif mode == SQUARE_MODE_RIGHTBOTTOM:
            self.rightbottom()
        else: print('wrong mode')
            
    '''
        (0,1)         (6,7)
        *-------------*
        |             |
        |      x      |
        |             |
        *-------------*
        (2,3)         (4,5)
    '''
    def center(self):
        half = self.edge*0.5
        self.center = (self.sx, self.sy)
        self.vertex.put([0,2], self.sx-half)
        self.vertex.put([4,6], self.sx+half)
        self.vertex.put([1,7], self.sy+half)
        self.vertex.put([3,5], self.sy-half)
            
    def lefttop(self):
        half = self.edge/2.
        self.center = (self.sx+half, self.y-half)
        self.vertex.put([0,2], self.sx)
        self.vertex.put([4,6], self.x+self.edge)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy-self.edge)
    
    def righttop(self):
        half = self.edge/2.
        self.center = (self.sx-half, self.sy-half)
        self.vertex.put([0,2], self.sx-self.edge)
        self.vertex.put([4,6], self.sx)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy-self.edge)
    
    def leftbottom(self):
        half = self.edge/2.
        self.center = (self.sx+half, self.sy+half)
        self.vertex.put([0,2], self.sx)
        self.vertex.put([4,6], self.sx+self.edge)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy+self.edge)	
        
    def rightbottom(self):
        half = self.edge/2.
        self.center = (self.sx-half, self.sy-half)
        self.vertex.put([0,2], self.sx)
        self.vertex.put([4,6], self.sx-self.edge)
        self.vertex.put([1,7], self.sy)
        self.vertex.put([3,5], self.sy+self.edge)	

class EquiTriangle(shape.Shape):
    def __init__(self,xc,yc,edge,lcol=color.BLACK,lthk=0.001,fcol=None):
        super().__init__(xc,yc,3,edge,lcol,lthk,fcol)
        hgt = edge*np.sin(util.deg_to_rad(60))
        x1 = edge*0.5
        # lower left v1
        self.vertex[0] = xc-x1
        self.vertex[1] = yc-hgt*0.5
        
        # lower right v2
        self.vertex[2] = xc+x1
        self.vertex[3] = yc-hgt*0.5

        # center up v3
        self.vertex[4] = xc
        self.vertex[5] = yc+hgt*0.5
        
class Polygon(shape.Shape):
    def __init__(self,
                xc, yc, 
                nvert, 
                edge, 
                lcol=color.BLACK, 
                lthk=0.001,
                lpat=linepat._PAT_SOLID,
                pat_len=0.04, 
                fcol=None,
                deg_shift=0,
                ccw = True,
                end_point=False
        ):
        nvert1 = nvert if not end_point else nvert+1
        super().__init__( xc,yc, 
                          nvert1, 
                          edge, 
                          lcol, 
                          lthk, 
                          fcol, 
                          lpat, 
                          pat_len)
        step = 360.0/nvert
        cw = 1 if ccw else -1
        for i in range(nvert):
            rad = cw*rotation.deg_to_rad(i*step+deg_shift)
            self.vertex[i*2]=xc+edge*np.cos(rad)
            self.vertex[i*2+1]=yc+edge*np.sin(rad)
            
        if end_point:
            self.vertex[-1] = self.vertex[1]
            self.vertex[-2] = self.vertex[0]
            
    def __str__(self):
        return "x: %f\ny: %f\nnvert: %d\nedge: %f\n"\
               "lcol: %s\nlthk: %f\nfcol: %s\npat_len: %f\nlpat: %s\n"%\
        (self.xc, self.yc, self.nvert, self.edge, 
        self.lcol, self.lthk, self.fcol, self.pat_len, self.pat_t)

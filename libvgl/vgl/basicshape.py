'''
    basicshape.py
    
    7/11/2023 Added Arrowed Lines
    
'''
import numpy as np
from . import shape
from . import linepat
from . import linetype
from . import util
from . import color

_ARROWTYPE_OPEN         = 0x0001
_ARROWTYPE_CLOSED       = 0x0002
_ARROWTYPE_CLOSEDFILLED = 0x0003
_ARROWTYPE_CLOSEDBLANK  = 0x0004
_ARROWTYPE_DOT          = 0x0005
_ARROWTYPE_VIKING       = 0x0010|_ARROWTYPE_CLOSED
_ARROWTYPE_VIKINGFILLED = 0x0010|_ARROWTYPE_CLOSEDFILLED
_ARROWTYPE_VIKINGBLANK  = 0x0010|_ARROWTYPE_CLOSEDBLANK

_ARROWPOS_START         = 0x0100
_ARROWPOS_END           = 0x0101

_HEAD_CLOSED       = lambda b : b & _ARROWTYPE_CLOSED
_HEAD_CLOSEDFILLED = lambda b : b & _ARROWTYPE_CLOSEDFILLED
_HEAD_CLOSEDBLANK  = lambda b : b & _ARROWTYPE_CLOSEDBLANK

_arrow_angle         = 15 # degree
_arrow_length_0      = 0.01 # 
_arrow_length_1      = 0.05 # 
_viking_xpos_scale   = 0.7
#_arrowhead_start = "START"
#_arrowhead_end = "END"

BOX_POS_CENTER      = 0x100000 
BOX_POS_LEFTTOP     = 0x100001
BOX_POS_LEFTBOTTOM  = 0x100002
BOX_POS_RIGHTTOP    = 0x100003
BOX_POS_RIGHTBOTTOM = 0x100004
 
 
class ArrowHead():
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey,
                 show   = True,
                 col    = color.BLACK,
                 pos_t  = _ARROWPOS_START, 
                 type_t = _ARROWTYPE_OPEN, 
                 angle  = _arrow_angle, 
                 length = _arrow_length_1):
                 
        self.show   = show
        self.pos_t  = pos_t
        self.type_t = type_t
        self.angle  = angle # degree
        self.length = length # length of arrow head
        self.col    = col
        
        self.calculate_pos(frm, sx, sy, ex, ey)
        
    def set(self, col, type_t, angle, length):
        self.type_t = type_t
        self.angle  = angle # degree
        self.length = length # length of arrow head
        self.col    = col
        
        
    def calculate_pos(self, frm, sx, sy, ex, ey):
    
        theta = np.arctan2(ey-sy, ex-sx)
        
        # find arrow head wing pos in local coord
        wing = self.length*frm.hgt()
        wing_x = wing*np.cos(util.deg_to_rad(self.angle))
        wing_y = wing*np.sin(util.deg_to_rad(self.angle))
        vk_x   = wing_x*_viking_xpos_scale
        vk_y   = 0
        
        if self.pos_t == _ARROWPOS_START:
            self.wing_up   = util.rad_rotation(wing_x,  wing_y, -theta)
            self.wing_down = util.rad_rotation(wing_x, -wing_y, -theta)
            self.vk        = util.rad_rotation(  vk_x,    vk_y, -theta)
        else:
            self.wing_up   = util.rad_rotation(-wing_x,  wing_y, -theta)
            self.wing_down = util.rad_rotation(-wing_x, -wing_y, -theta)
            self.vk        = util.rad_rotation(  -vk_x,    vk_y, -theta)
            
def draw_arrow_head(dev, sx, sy, arrow, lcol, lthk, viewport):
    
    sx = dev._x_viewport(sx) if viewport==False else sx
    sy = dev._y_viewport(sy) if viewport==False else sy
    xs = [sx+arrow.wing_up[0], sx, sx+arrow.wing_down[0], sx+arrow.wing_up[0]]
    
    if viewport == False:
        ys = [sy+arrow.wing_up[1], sy, sy+arrow.wing_down[1], sy+arrow.wing_up[1]]
        vky= sy+arrow.vk[1]
    else:
        ys = [sy-arrow.wing_up[1], sy, sy-arrow.wing_down[1], sy-arrow.wing_up[1]]
        vky= sy-arrow.vk[1]

    if arrow.type_t == _ARROWTYPE_VIKING or\
       arrow.type_t == _ARROWTYPE_VIKINGFILLED or\
       arrow.type_t == _ARROWTYPE_VIKINGBLANK:
        xs.insert(-1,sx+arrow.vk[0])
        ys.insert(-1,vky)
        
    # open
    if arrow.type_t == _ARROWTYPE_OPEN:
        dev.lpolyline(xs[:3], ys[:3], lcol, lthk)
        
    #elif arrow.type_t == _ARROWTYPE_CLOSED:
    elif _HEAD_CLOSED(arrow.type_t):
        dev.lpolygon(xs, ys, lcol=lcol, lthk=lthk, fcol=None)
        
    #elif arrow.type_t == _ARROWTYPE_CLOSEDFILLED:
    elif _HEAD_CLOSEDFILLED(arrow.type_t):
        dev.lpolygon(xs, ys, lcol=lcol, lthk=lthk, fcol=lcol)
        
    #elif arrow.type_t == _ARROWTYPE_CLOSEDBLANK:
    elif _HEAD_CLOSEDBLANK(arrow.type_t):
        dev.lpolygon(xs, ys, lcol=lcol, lthk=lthk, fcol=color.WHITE)

# lcol, lthk, len_pat, pat_t
class GenericLine(linetype.LineLevelC):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol      = color.BLACK,
                 lthk      = 0.001,
                 lpat      = linepat._PAT_SOLID,
                 pat_len   = 0.04,
                 show      = False,
                 col       = color.BLACK,
                 type_t    = _ARROWTYPE_OPEN, 
                 angle     = _arrow_angle, 
                 length    = _arrow_length_1, 
                 viewport  = False):
                 
        super().__init__(lcol=lcol, lthk=lthk, lpat=lpat, pat_len=pat_len)
        
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.viewport = viewport
        self.begin_arrow = ArrowHead(frm, sx,sy,ex,ey, 
                                     show, col, _ARROWPOS_START, type_t, angle, length)
        self.end_arrow   = ArrowHead(frm, sx,sy,ex,ey, 
                                     show, col, _ARROWPOS_END, type_t, angle, length)
    def __str__(self):
        return "Lcol : %s\nLthk : %f\nLpat : %s\nPat_len : %f\nShow : %s\n"\
               "Col  : %s\nType : %s\nAngle: %f\nLength: %f\nViewport : %s"%(
               str(self.lcol), 
               self.lthk, 
               self.lpat, 
               self.pat_len, 
               self.end_arrow.show,
               str(self.end_arrow.col) , 
               self.end_arrow.type_t, 
               self.end_arrow.angle, 
               self.end_arrow.length, 
               self.viewport)
    
    def draw(self, dev):
        if self.viewport == False:
            dev.line(self.sx, self.sy, self.ex, self.ey, 
                     self.lcol, self.lthk, lpat=self.get_line_pattern())
        else:
            dev.lline(self.sx, self.sy, self.ex, self.ey, 
                      self.lcol, self.lthk, lpat=self.get_line_pattern())

        if self.begin_arrow.show:
            acol = self.lcol if self.begin_arrow.col == self.lcol\
                             else self.begin_arrow.col
            draw_arrow_head(dev, self.sx, self.sy, self.begin_arrow, 
            acol, self.lthk, self.viewport)
            
        if self.end_arrow.show:
            acol = self.lcol if   self.end_arrow.col == self.lcol\
                             else self.end_arrow.col
            draw_arrow_head(dev, self.ex, self.ey, self.end_arrow, 
            acol, self.lthk, self.viewport)

class ArrowLine(GenericLine):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,                 
                 show     = True,
                 col      = color.BLACK,
                 type_t   = _ARROWTYPE_OPEN, 
                 angle    = _arrow_angle, 
                 length   = _arrow_length_1, 
                 viewport = False):
                 
        super().__init__(frm, 
                         sx, 
                         sy, 
                         ex, 
                         ey, 
                         lcol    = lcol, 
                         lthk    = lthk, 
                         lpat    = lpat, 
                         pat_len = pat_len,
                         show    = show, 
                         col     = col, 
                         type_t  = type_t, 
                         angle   = angle, 
                         length  = length, 
                         viewport= viewport)
        
class BeginArrowLine(GenericLine):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,                 
                 show     = True,
                 col      = color.BLACK,
                 type_t   = _ARROWTYPE_OPEN, 
                 angle    = _arrow_angle, 
                 length   = _arrow_length_1,
                 viewport = False):
                 
        super().__init__(frm, 
                         sx, 
                         sy, 
                         ex, 
                         ey, 
                         lcol    = lcol, 
                         lthk    = lthk, 
                         lpat    = lpat, 
                         pat_len = pat_len,
                         show    = show, 
                         col     = col, 
                         type_t  = type_t, 
                         angle   = angle, 
                         length  = length, 
                         viewport= viewport)
        self.end_arrow.show = False
        
class EndArrowLine(GenericLine):
    def __init__(self, 
                 frm, 
                 sx, 
                 sy, 
                 ex, 
                 ey, 
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,                 
                 show     = True,
                 col      = color.BLACK,
                 type_t   = _ARROWTYPE_OPEN, 
                 angle    = _arrow_angle, 
                 length   = _arrow_length_1,
                 viewport = False):
                 
        super().__init__(frm, sx, sy, ex, ey, 
                         lcol    = lcol, 
                         lthk    = lthk, 
                         lpat    = lpat, 
                         pat_len = pat_len,
                         show    = show, 
                         col     = col, 
                         type_t  = type_t, 
                         angle   = angle, 
                         length  = length, 
                         viewport= viewport)
        self.begin_arrow.show = False
 
class Box(shape.Shape):
    def __init__(self, 
                 sx, 
                 sy, 
                 wid      = 1,  # edge length
                 hgt      = 1,  # edge length
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 fcol     = None, 
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,  
                 viewport = False,
                 pos_t    = BOX_POS_LEFTBOTTOM, 
                 src      = None):
        
        super().__init__(sx, sy, 4, wid, 
                         lcol=lcol, lthk=lthk, fcol=fcol, lpat=lpat, pat_len=pat_len)
        self.wid= wid
        self.hgt= hgt
        self.viewport = viewport
        
        # copy Box to Box
        # need to check if size not equal
        if isinstance(src, Box):
            self.vertex[:] = src.vertex[:]
        elif isinstance(src, np.ndarray):
            self.vertex[:] = src[:]
        elif isinstance(src, list):
            self.vertex = np.array(src)
        else:
            if   pos_t == BOX_POS_LEFTBOTTOM : self.leftbottom()
            elif pos_t == BOX_POS_LEFTTOP    : self.lefttop()
            elif pos_t == BOX_POS_RIGHTBOTTOM: self.rightbottom()
            elif pos_t == BOX_POS_RIGHTTOP   : self.righttop()
            elif pos_t == BOX_POS_CENTER     : self.center()
            
    def copy(self):
        return Box( self.sx, 
                    self.sy,
                    self.wid,
                    self.hgt,
                    self.lcol,
                    self.lthk,
                    self.fcol,
                    self.lpat,
                    self.pat_len,
                    self.viewport,
                    src = self.vertex )
    #
    # v1 ---- v4
    # |        |
    # |        |
    # v2 ---- v3
    #
    # vertex order: v1 --> v2 --> v3 --> v4
    
    def center(self):
        hw = self.wid*0.5
        hh = self.hgt*0.5
        self.vertex.put([0,2,4,6], [self.sx-hw, 
                                    self.sx+hw, 
                                    self.sx+hw, 
                                    self.sx-hw ])
        self.vertex.put([1,3,5,7], [self.sy-hh, 
                                    self.sy-hh, 
                                    self.sy+hh, 
                                    self.sy+hh])
        return self
        
    def lefttop(self):
        self.vertex.put([0,2,4,6], [self.sx, 
                                    self.sx, 
                                    self.sx+self.wid, 
                                    self.sx+self.wid ])
                                    
        self.vertex.put([1,3,5,7], [self.sy,
                                    self.sy-self.hgt, 
                                    self.sy-self.hgt, 
                                    self.sy])
        return self
        
    def righttop(self):
        self.vertex.put([0,2,4,6], [self.sx-self.wid, 
                                    self.sx-self.wid, 
                                    self.sx, 
                                    self.sx ])
                                    
        self.vertex.put([1,3,5,7], [self.sy,
                                    self.sy-self.hgt, 
                                    self.sy-self.hgt, 
                                    self.sy])
        return self
        
    def leftbottom(self):
        self.vertex.put([0,2,4,6], [self.sx, 
                                    self.sx+self.wid, 
                                    self.sx+self.wid, 
                                    self.sx ])
                                    
        self.vertex.put([1,3,5,7], [self.sy,
                                    self.sy, 
                                    self.sy+self.hgt, 
                                    self.sy+self.hgt])
        return self
        
    def rightbottom(self):
        self.vertex.put([0,2,4,6], [self.sx-self.wid, 
                                    self.sx, 
                                    self.sx, 
                                    self.sx-self.wid])
                                    
        self.vertex.put([1,3,5,7], [self.sy,
                                    self.sy, 
                                    self.sy+self.hgt, 
                                    self.sy+self.hgt])
        return self
        
    def draw(self, dev):
        if self.viewport==True:
            dev.lpolygon(self.get_xs(), self.get_ys(), 
                         self.lcol, self.lthk, self.lpat, self.fcol)
        else:
            dev.polygon(self.get_xs(), self.get_ys(), 
                        self.lcol, self.lthk, self.lpat, self.fcol)
        
        
class StarPolygon(shape.Shape):
    def __init__(self, 
                 sx, 
                 sy, 
                 nvert=5,
                 radius  = 1, # length from center to a vertex
                 lcol     = color.BLACK,
                 lthk     = 0.001,
                 fcol     = None, 
                 lpat     = linepat._PAT_SOLID,
                 pat_len  = 0.04,  
                 viewport = False):  
         
        if nvert < 3:
            raise ValueError('nvert must be greater than equal 3')
            
        super().__init__(sx, sy, nvert*2, radius, 
                         lcol=lcol, lthk=lthk, fcol=fcol, lpat=lpat, pat_len=pat_len)
        self.viewport = viewport
        self.nvert = nvert
        self.radius = radius
        self._u_vertex = np.zeros(nvert*2)
        self.reset_pvertex()
        self.reset_uvertex()
        
    def update(self, sx, sy):
        self.sx = sx
        self.sy = sy
        self.reset_pvertex()
        self.reset_uvertex()
      
    def reset(self):
        self.reset_pvertex()
        self.reset_uvertex()
        
    def reset_pvertex(self): 
        for k in range(self.nvert):
            angle = 0.5*(4*k+self.nvert)*np.pi/self.nvert
            self.vertex[k*4] = self.sx+self.radius*np.cos(angle) 
            self.vertex[k*4+1] = self.sy+self.radius*np.sin(angle)

    def reset_uvertex(self):
        nvert = self.nvert
        xx = self.vertex[0::4]
        yy = self.vertex[1::4]

        if nvert == 3 or nvert == 4:
            default_u = nvert*0.1
            for i in range(nvert):
                #angle = np.pi*(0.75+0.5*i)
                angle = 2*np.pi*(i+1)/nvert+0.5*(nvert-2)*np.pi/nvert
                px = self.sx + default_u*self.radius*np.cos(angle)
                py = self.sy + default_u*self.radius*np.sin(angle)
                self.vertex[2+i*4] = px
                self.vertex[2+i*4+1] = py
                self._u_vertex[i*2] = px
                self._u_vertex[i*2+1] = py
        else:
            for i in range(nvert):
                i1 = i
                i2 = (i+2)%nvert
                i3 = (i+1)%nvert
                i4 = (nvert-1+i)%nvert
            
                x1, y1 = xx[i1], yy[i1]
                x2, y2 = xx[i2], yy[i2]
                x3, y3 = xx[i3], yy[i3]
                x4, y4 = xx[i4], yy[i4]
            
                if abs(x2-x1) < 1e-10:
                    m = (y4-y3)/(x4-x3)
                    px= x1
                    py= m*(px-x3)+y3
    
                elif abs(x4-x3) < 1e-10:
                    m = (y2-y1)/(x2-x1)
                    px= x3
                    py= m*(px-x1)+y1
    
                else:
                    m1 = (y2-y1)/(x2-x1)
                    m2 = (y4-y3)/(x4-x3)
                    px = (m1*x1-y1-m2*x3+y3)/(m1-m2)
                    py = m1*(px-x1)+y1
                
                self.vertex[2+i*4] = px
                self.vertex[2+i*4+1] = py
                self._u_vertex[i*2] = px
                self._u_vertex[i*2+1] = py
    
    @property
    def pxs(self):
        return self.vertex[0::4]
        
    @property
    def pys(self):
        return self.vertex[1::4]
        
    @property
    def uxs(self):
        return self.vertex[2::4]

    @property
    def uys(self):
        return self.vertex[3::4]
        
    @property
    def u_radius(self):
        return np.sqrt(self.vertex[2]**2+self.vertex[3]**2)
        
    @property
    def u_param(self):
        return self._param_u
        
    # u -> 1 : inner radius
    # u < 1, u =1, u > 1
    @u_param.setter
    def u_param(self, u):
        for i in range(self.nvert):
            self.vertex[2+i*4] = self.sx+(self._u_vertex[i*2]-self.sx)*u
            self.vertex[2+i*4+1] = self.sy+(self._u_vertex[i*2+1]-self.sy)*u
        

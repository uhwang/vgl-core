# Vector Graphic Library (VGL) for Python
#
# symbol.py
#
# 2020-2-12 Ver 0.1
#
# Author: Uisang Hwang
# Email : uhwangtx@gmail.com
#
from numpy import pi, sin, cos, flip, copy

from . import color
from . import vertex
from . import starpolygon
from . import affine
from .rotation import deg_to_rad

symbol_name = [
    ('circle'        , 'o'),
    ('triangle_left' , '<'),
    ('triangle_right', '>'),
    ('triangle_down' , 'v'),
    ('triangle_up'   , '^'),
    ('diamond'       , 'D'),
    ('square'        , 's'),
    ('pentagon'      , 'p'),
    ('trigram'       , '*3'),
    ('quadgram'      , '*4'),
    ('pentagram'     , '*5'),
    ('hexgram'       , '*6'),
    ('plus'          , '+'),
    ('cross'         , 'x')
]

symbol_circle_name         = symbol_name[0][0]
symbol_triangle_left_name  = symbol_name[1][0]
symbol_triangle_right_name = symbol_name[2][0]
symbol_triangle_down_name  = symbol_name[3][0]
symbol_triangle_up_name    = symbol_name[4][0]
symbol_diamond_name        = symbol_name[5][0]
symbol_square_name         = symbol_name[6][0]
symbol_pentagon_name       = symbol_name[7][0]
symbol_trigram_name        = symbol_name[8][0]
symbol_quadgram_name       = symbol_name[9][0]
symbol_pentagram_name      = symbol_name[10][0]
symbol_hexgram_name        = symbol_name[11][0]
symbol_plus_name           = symbol_name[12][0]
symbol_cross_name          = symbol_name[13][0]

symbol_string = ','.join([ c[1] for c in symbol_name])
get_symbol_name = {s[1]:s[0] for s in symbol_name}


class Symbol(vertex.Vertex):
    def __init__(self, name, nvert, size, lcol, lthk, fill, fcol):
        super().__init__(nvert)
        self.name     = name
        self.lcol     = lcol
        self.lthk     = lthk
        self.fill     = fill
        self.fcol     = fcol
        self.size     = size

    def __repr__(self):
        return "Name: %s\n"\
                "Lcol: %s\n"\
                "Lthk: %f\n"\
                "Fill: %s\n"\
                "Fcol: %s\n"\
                "Size: %f"%(\
                self.name,
                str(self.lcol),
                self.lthk,
                self.fill,
                str(self.fcol),
                self.size)
        
    def set_lcolor(self, col): self.lcol = col
    def set_fcolor(self, col): self.fcol = col
    def update_xy(self, x,y):
        return self.vertex[::2]+x, self.vertex[1::2]+y
    def set_color(self, lcol, fcol):
        self.lcol = lcol
        self.fcol = fcol
    def set_color_all(self, col):
        self.set_color(col,col)
    
class Circle(Symbol):
    def __init__(
                    self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        super().__init__(symbol_circle_name,12,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
            
    def update(self, x,y):
        nvert = self.get_nvertex()
        len= self.hgt * self.size
        step = 360.0/nvert
        for i in range(nvert):
            rad = deg_to_rad(i*step)
            self.vertex[i*2]=x+len*cos(rad)
            self.vertex[i*2+1]=y+len*sin(rad)
            
class TriangleDown(Symbol):
    def __init__(
                    self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        super().__init__(symbol_triangle_down_name,3,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
            
    def update(self, x,y):
        len= self.hgt * self.size
        hgt = len * 0.8660254
        hs=len*0.5
        hh=hgt*0.51
        
        self.vertex[0]=x-hs
        self.vertex[1]=y-hh
        self.vertex[2]=x
        self.vertex[3]=y+hh
        self.vertex[4]=x+hs
        self.vertex[5]=y-hh

class TriangleUp(Symbol):
    def __init__(
                    self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        super().__init__(symbol_triangle_down_name,3,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
            
    def update(self, x,y):
        len= self.hgt * self.size
        hgt = len * 0.8660254
        hs=len*0.5
        hh=hgt*0.5
        
        self.vertex[0]=x-hs
        self.vertex[1]=y-hh
        self.vertex[2]=x+hs
        self.vertex[3]=y-hh
        self.vertex[4]=x
        self.vertex[5]=y+hh
        
class TriangleRight(Symbol):
    def __init__(
                    self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        super().__init__(symbol_triangle_right_name,3,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
    
    def update(self, x, y):
        len= self.hgt * self.size
        hgt = len * 0.8660254
        hs=len*0.5
        hh=hgt*0.51
    
        self.vertex[0]=x-hh
        self.vertex[1]=y+hs
        self.vertex[2]=x-hh
        self.vertex[3]=y-hs
        self.vertex[4]=x+hh
        self.vertex[5]=y
        
class TriangleLeft(Symbol):
    def __init__(
                    self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        super().__init__(symbol_triangle_left_name,3,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
        
    def update(self, x, y):
        len= self.hgt * self.size
        hgt = len * 0.8660254
        hs=len*0.5
        hh=hgt*0.51
    
        self.vertex[0]=x-hh
        self.vertex[1]=y
        self.vertex[2]=x+hh
        self.vertex[3]=y-hs
        self.vertex[4]=x+hh
        self.vertex[5]=y+hs

class Diamond(Symbol):
    def __init__(
                    self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        super().__init__(symbol_diamond_name,4,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
        
    def update(self, x, y):
        len= self.hgt * self.size
        hh=0.546*len
        
        self.vertex[0]=x
        self.vertex[1]=y+hh
        self.vertex[2]=x-hh
        self.vertex[3]=y
        self.vertex[4]=x
        self.vertex[5]=y-hh
        self.vertex[6]=x+hh
        self.vertex[7]=y
        
class Square(Symbol):
    def __init__(
                    self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        super().__init__(symbol_square_name,4,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
        
    def update(self, x, y):
        len= self.hgt * self.size
        hh=0.5*len
        
        self.vertex[0]=x-hh
        self.vertex[1]=y+hh
        self.vertex[2]=x-hh
        self.vertex[3]=y-hh
        self.vertex[4]=x+hh
        self.vertex[5]=y-hh
        self.vertex[6]=x+hh
        self.vertex[7]=y+hh
    
class Pentagon(Symbol):
    def __init__(self, 
                    size, 
                    hgt, 
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        
        super().__init__(symbol_pentagon_name,5,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
        
    def update(self, x, y):
        step = 360.0/self.nvert
        deg_shift = 180*(0.5-2/self.nvert)
        edge = self.hgt * self.size
        for i in range(self.nvert):
            rad = deg_to_rad(i*step+deg_shift)
            self.vertex[i*2]=x+edge*cos(rad)
            self.vertex[i*2+1]=y+edge*sin(rad)
    
class Star(Symbol):
    def __init__(self, 
                    size, 
                    hgt,
                    nvert = 5,
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED,
                    param_u = None
                ):
        
        super().__init__(symbol_pentagon_name,nvert*2,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.param_u = param_u
        self.update(0,0)
        
    def update(self, x, y):
        radius = self.hgt * self.size
        starpolygon.create_star_polygon(x, y, int(self.nvert/2), radius, self.vertex, self.param_u)
        
class Plus(Symbol):
    def __init__(self, 
                    size, 
                    hgt,
                    nvert = 12,
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        
        super().__init__(symbol_plus_name,nvert,size,lcol,lthk,True,fcol)
        self.hgt = hgt
        self.update(0,0)
    
    def update(self,x,y):
        edge = self.hgt * self.size
        h = edge*0.25
        self.vertex[0] = 2*h
        self.vertex[1] = h*0.6
        self.vertex[2] = h*0.6
        self.vertex[3] = h*0.6
        self.vertex[4] = h*0.6
        self.vertex[5] = 2*h

        xx, yy = self.vertex[0:6:2], self.vertex[1:7:2]
        x_, y_ = affine.mirror_o(xx, yy, True)

        # 2nd quadrant: y-mirror
        self.vertex[6:11:2] = flip(x_)
        self.vertex[7:12:2] = flip(yy)
        # 3rd quadrant: origin-mirror
        self.vertex[12:17:2] = x_
        self.vertex[13:18:2] = y_
        # 4th quadrant: origin-mirror
        self.vertex[18:24:2] = flip(xx)
        self.vertex[19:24:2] = flip(y_)

class Cross(Plus):
    def __init__(self, 
                    size, 
                    hgt,
                    nvert = 12,
                    lcol=color.BLACK,
                    lthk=0.001,
                    fill=True,
                    fcol=color.RED
                ):
        
        super().__init__(size,hgt,nvert,lcol,lthk,True,fcol)
        self.name = symbol_cross_name
        self.rotate(45)
        
    def update(self,x,y):
        super().update(x,y)
        self.rotate(45)
        
        
stock_symbol = {
    symbol_circle_name : Circle(3, 0.05),
    symbol_triangle_left_name : TriangleLeft(3, 0.05),
    symbol_triangle_right_name : TriangleRight(3, 0.05),
    symbol_triangle_down_name : TriangleDown(3, 0.05),
    symbol_triangle_up_name : TriangleUp(3, 0.05),
    symbol_diamond_name : Diamond(3, 0.05),
    symbol_square_name : Square(3, 0.05),
    symbol_pentagon_name : Pentagon(3, 0.05),
    symbol_trigram_name : Star(3, 0.05, nvert=3),
    symbol_quadgram_name : Star(3, 0.05, nvert=4),
    symbol_pentagram_name : Star(3, 0.05, nvert=5),
    symbol_hexgram_name : Star(3, 0.05, nvert=6),
    symbol_plus_name : Plus(3, 0.05),
    symbol_cross_name : Cross(3, 0.05),
}
    
            
        

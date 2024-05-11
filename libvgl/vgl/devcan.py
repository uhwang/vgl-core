'''
    devicanv.py
    
    03/10/2023  Separate device file

'''
import numpy as np
from ipycanvas import Canvas        
from . import color
from . import device
from . import linepat
from . import patline
from . gdiobj import Pen, Brush
        
class DeviceIPycanvas(device.DeviceRaster):
    def __init__(self, gbox, dpi):
        super().__init__(gbox, dpi)
        self.pen     = Pen()
        self.prv_pen = Pen()
        self.brush   = Brush()
        self.npos    = 0
        self.canvas  = Canvas(width=self.gwid, height=self.ghgt)
        self.lcol    = color.WHITE
        self.fcol    = color.WHITE
        self.nlineto = 0
        
    def set_device(self, frm, extend=device._FIT_NONE):
        self.set_plot(frm, extend)
                
    def set_pixel(self, x, y, col):
        pass
        
    def fill_black(self):
        self.canvas.fill_style = color.get_style(color.BLACK)
        self.canvas.fill_rect(0,0, self.canvas.width, self.canvas.height)

    def fill_white(self):
        self.canvas.fill_style = color.get_style(color.WHITE)
        self.canvas.fill_rect(0,0, self.canvas.width, self.canvas.height)

    def fill_cyan(self):
        self.canvas.fill_style = color.get_style(color.CYAN)
        self.canvas.fill_rect(0,0, self.canvas.width, self.canvas.height)
        
    def make_pen(self, lcol, lthk):
        self.pen.lthk = lthk
        self.pen.lcol = lcol
        self.canvas.stroke_style = color.get_style(lcol)
        self.canvas.line_width = self.get_xl(lthk)
        
    def make_brush(self, fcol):
        self.canvas.fill_style = color.get_style(fcol)
        self.brush.fcol = fcol
        
    def delete_pen(self):
        self.pen.lcol = None
        self.pen.lthk = None
        
    def delete_brush(self):
        self.brush.fcol = None
        
    def _moveto(self, x, y, viewport = False):
        if self.nlineto > 0:
            self.canvas.stroke()
            self.nlineto = 0

        self.canvas.begin_path()
        self.canvas.move_to(dev.get_xl(x) if viewport else dev._x_pixel(x),
                            dev.get_yl(y) if viewport else dev._y_pixel(y))
        
    def _lineto(self, x, y, viewport = False):
        self.canvas.line_to(dev.get_xl(x) if viewport else dev._x_pixel(x),
                            dev.get_yl(y) if viewport else dev._y_pixel(y))
        self.nlineto += 1

    def moveto(self, x, y):
        self._moveto(x,y)

    def lmoveto(self, x, y):
        self._moveto(x,y,True)

    def lineto(self, x,y):
        self._lineto(x,y)

    def llineto(self,x,y):
        self._lineto(x,y,True)

    def stroke(self):
        if self.nlineto > 0:
            self.canvas.stroke()
            
        return self.canvas
        
    def create_pnt_list(self, x, y, convx, convy, pnt_type_tuple=False):
        if pnt_type_tuple:
            self.points= [(convx(x1), convy(y1)) for x1, y1 in zip(x,y)]
        else:
            self.points= [[convx(x1), convy(y1)] for x1, y1 in zip(x,y)]
    
    def draw_geometry(self, lcol, lthk, lpat, fcol):

        if fcol or self.brush.fcol: 
            if fcol: self.make_brush(fcol)
            self.canvas.fill_polygon(self.points)
            self.delete_brush()
            
        if lcol or self.pen.lcol:
            if lcol: self.make_pen(lcol, lthk)
            self.canvas.stroke_polygon(self.points)
            self.delete_pen()
        
    def polygon(self, x, y, lcol=color.BLACK, 
                            lthk=0.001, 
                            lpat=linepat._PAT_SOLID, 
                            fcol=None, 
                            viewport=False):
                            
        self._polyline(x,y,lcol,lthk,lpat,fcol,True,viewport)

    def polyline(self, x,y,
                       lcol=color.BLACK,
                       lthk=0.001, 
                       lpat=linepat._PAT_SOLID):
        self._polyline(x,y,lcol,lthk,lpat,None,False,False)
        
    def _polyline(self, 
                 x, y, 
                 lcol=color.BLACK,
                 lthk=0.001, 
                 lpat=linepat._PAT_SOLID,
                 fcol=None,                 
                 closed=False,
                 viewport=False):
                 
        # closed : draw polygon
        if closed:
            if isinstance(x, np.ndarray):
                xp = np.append(x, x[0])
                yp = np.append(y, y[0])
            elif isinstance(x, list):
                xp = x.copy()
                yp = y.copy()
                xp.append(x[0])
                yp.append(y[0])
        else:
            xp, yp = x, y
    
        if viewport:
            self.create_pnt_list(xp, yp, self.get_xl, self.get_yl, True)
        else:
            self.create_pnt_list(xp, yp, self._x_pixel, self._y_pixel, True)

        # fill polygon
        if closed and isinstance(fcol, color.Color):
            self.canvas.fill_style = color.get_style(fcol)
            self.canvas.fill_polygon(self.points)
            if lcol is None:
                self.canvas.stroke_style = color.get_style(fcol)
                self.canvas.stroke_polygon(self.points)
                self.canvas.close_path()
                
        # patterned line
        if isinstance(lpat, linepat.LinePattern):
            if not isinstance(self.pen.lcol, color.Color):
                self.make_pen(lcol, lthk*self.frm.hgt())
                
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, 
                                                             lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cavnas.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1[1:], y1[1:]):
                    self.cavnas.line_to(self.get_xl(x2),self.get_yl(y2))
                    
            if isinstance(self.pen.lcol, color.Color):
                self.delete_pen()            
        # solid line       
        else:
            if lcol: 
                self.make_pen(lcol, lthk*self.frm.hgt())
                self.canvas.stroke_lines(self.points)
                self.delete_pen()
        
    def begin(self,lcol,lthk,fcol): 
        return
        
    def end(self): 
        return
    
    def begin_symbol(self, sym): 
        self.make_pen(sym.lcol, sym.lthk)
        self.make_brush(sym.fcol)
        
    def end_symbol(self): 
        self.delete_brush()
        self.delete_pen()
    
    def circle(self, x,y, 
                     rad, 
                     lcol=color.BLACK, 
                     lthk=0.001, 
                     lpat=linepat._PAT_SOLID, 
                     fcol=None):
                     
        rrad = np.linspace(0, np.pi*2, self._circle_point)
        x1 = x+rad*np.cos(rrad)
        y1 = y+rad*np.sin(rrad)
        self._polyline(x1, y1, lcol, lthk, lpat, fcol, True, False)

    def symbol(self, x,y, sym):
        px, py = sym.update_xy(self._x_viewport(x),self._y_viewport(y))

        self._polyline(px,py,sym.lcol,sym.lthk,
                       linepat._PAT_SOLID, sym.fcol,True,True)

    def line(self, sx, sy, ex, ey, 
                   lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):
    
        xx, yy = [sx, ex], [sy, ey]
        self._polyline(xx,yy,lcol,lthk,lpat,None,False,False)
        
    def lline(self, sx, sy, ex, ey, 
                    lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):
    
        xx, yy = [sx,ex], [sy,ey]
        self._polyline(xx,yy,lcol,lthk,lpat,None,False,True)

    def lpolygon(self, x, y, 
                       lcol=color.BLACK, 
                       lthk=0.001, 
                       lpat=linepat._PAT_SOLID, 
                       fcol=None):
                       
        self._polyline(x,y,lcol,lthk,lpat,fcol,True,True)
        
    def lpolyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):
        
        self._polyline(x,y,lcol,lthk,lpat,None,False,True)
            
    def create_clip(self, x1, y1, x2, y2):
        self.canvas.save()
        sx=self.get_xl(x1)
        sy=self.get_yl(y1)
        ex=self.get_xl(x2)
        ey=self.get_yl(y2)
        self.canvas.stroke_rect(sx,sy,ex-sx,ey-sy)
        self.canvas.clip()
        #self.canvas.restore()
        
    def delete_clip(self):
        self.canvas.restore()
        
    def clip(self):    
        return    
    def close(self, format='png'):
        #self.canvas.clear()    
        return self.canvas
       
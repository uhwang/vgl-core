'''
    devcairo.py
    
    03/10/2023  Separate device file    

'''
import cairo
import numpy as np
from PIL import Image
import moviepy.editor as mpy

from . import device
from . import color
from . import linepat
from . import patline
from . import gdiobj

class DeviceIMG(device.DeviceRaster):
    def __init__(self, fname, gbox, dpi):
        super().__init__(gbox, dpi)
        self.fname  = fname
        self.pen    = gdiobj.Pen()
        self.prv_pen= gdiobj.Pen()
        self.brush  = gdiobj.Brush()
        self.data   = np.ndarray(shape=(int(self.ghgt), int(self.gwid)), dtype=np.uint32)
        self.surf   = cairo.ImageSurface.create_for_data(self.data, 
                      cairo.FORMAT_ARGB32, int(self.gwid), int(self.ghgt))
        self.cntx   = cairo.Context(self.surf)
        self.lcol   = color.WHITE
        self.fcol   = color.WHITE
        self.fill_white()
        self.nlineto = 0
    
    def set_device(self, frm, extend=device._FIT_NONE):
        self.set_plot(frm, extend)
        
    def set_surface_pixel(self, x, y, col):
        self.data[y][x] = int("0xFF%02X%02X%02X"%(col.r,col.g,col.b),16)
        
    def set_pixel(self, x, y, col):
        self.set_surface_pixel(self.get_xp(x), self.get_yp(y), col)
        
    def fill_black(self):
        self.data[::]=0xff000000

    def fill_white(self):
        self.data[::]=0x0ffffffff

    def fill_cyan(self):
        self.data[::]=0xff00ffff
    
    def make_pen(self, lcol, lthk):
        self.pen.lthk = lthk
        self.pen.lcol = lcol
        c = color.normalize(lcol)
        self.cntx.set_source_rgb(c.r,c.g,c.b)
        self.cntx.set_line_width(self.get_ylt(lthk))
        
    def make_brush(self, fcol):
        self.fcol = color.normalize(fcol)
        self.cntx.set_source_rgb(self.fcol.r,self.fcol.g,self.fcol.b)
        self.brush.fcol = fcol
        
    def delete_pen(self):
        self.pen.lcol = None
        self.pen.lthk = None
        
    def delete_brush(self):
        self.brush.fcol = None
        
    def line(self, sx, sy, ex, ey, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID):
        pen_created = False
        if not isinstance(self.pen.lcol, color.Color) and lcol:
            self.make_pen(lcol, lthk*self.frm.hgt())
            pen_created = True

        if isinstance(lpat, linepat.LinePattern):
            xp = [sx, ex]
            yp = [sy, ey]
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1, y1):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
                self.cntx.stroke()
        else:
            self.cntx.move_to(self._x_pixel(sx),self._y_pixel(sy))
            self.cntx.line_to(self._x_pixel(ex),self._y_pixel(ey))
            self.cntx.stroke()
            
        if pen_created:
            self.delete_pen()
        
    def moveto(self, x, y):
        self.cntx.move_to(self._x_pixel(x),self._y_pixel(y))
        
    def lineto(self, x, y):
        self.cntx.line_to(self._x_pixel(x),self._y_pixel(y))
        self.nlineto += 1

    def stroke(self):
        self.cntx.stroke()
        
    def create_pnt_list(self, x, y, convx, convy):
        self.npnt = len(x)
        self.cntx.move_to(convx(x[0]), convy(y[0]))
        for x1, y1 in zip(x[1:], y[1:]):
            self.cntx.line_to(convx(x1), convy(y1))
    
    def draw_geometry(self, lcol, lthk, lpat, fcol):
        if fcol or self.brush.fcol: 
            if fcol: 
                self.make_brush(fcol)
            elif self.brush.fcol:
                self.make_brush(self.brush.fcol)
            
            if lpat==linepat._PAT_SOLID and (lcol or self.pen.lcol):
                self.cntx.fill_preserve()
            else:
                self.cntx.fill()
            
        if lpat==linepat._PAT_SOLID and (lcol or self.pen.lcol):
            if lcol: 
                self.make_pen(lcol, lthk)
            self.cntx.stroke()
        
        if lcol: self.delete_pen()
        if fcol: self.delete_brush()
        
    def polygon(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None, viewport=False):
        if (lpat == linepat._PAT_SOLID and lcol) or fcol:
            if viewport:
                self.create_pnt_list(x,y,self.get_xl,self.get_yl)
            else:
                self.create_pnt_list(x,y,self._x_pixel,self._y_pixel)
            self.cntx.close_path()        
            self.draw_geometry(lcol, lthk*self.frm.hgt(), lpat, fcol)

        if lcol and isinstance(lpat, linepat.LinePattern):
            if isinstance(x, np.ndarray):
                xp = np.append(x, x[0])
                yp = np.append(y, y[0])
            elif isinstance(x, list):
                xp = x.copy()
                yp = y.copy()
                xp.append(x[0])
                yp.append(y[0])
            if viewport:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport = True)
            else:
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            self.make_pen(lcol, lthk*self.frm.hgt())
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1, y1):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
            self.cntx.stroke()
            self.delete_pen()
            
    def polyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False):
    
        if isinstance(lpat, linepat.LinePattern):
            if not isinstance(self.pen.lcol, color.Color):
                self.make_pen(lcol, lthk)
                
            if closed:
                if isinstance(x, np.ndarray):
                    xp = np.append(x, x[0])
                    yp = np.append(x, y[0])
                elif isinstance(x, list):
                    xp = x.copy()
                    yp = y.copy()
                    xp.append(x[0])
                    yp.append(y[0])
            else:
                xp, yp = x, y
                
            pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1[1:], y1[1:]):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
                    
            if not isinstance(self.pen.lcol, color.Color):
                self.delete_pen()
        else:
            self.create_pnt_list(x,y,self._x_pixel,self._y_pixel)

            if closed: 
                self.cntx.close_path()
    
        if lcol: self.make_pen(lcol, lthk*self.frm.hgt())
        #else   : self.make_pen(self.pen.lcol, self.pen.lthk*self.frm.hgt())

        self.cntx.stroke()
            
        if lcol: self.delete_pen()
        
    def begin(self,lcol,lthk,fcol): 
        return
        
    def end(self): 
        return
    
    def begin_symbol(self, sym): 
        pass
        
    def end_symbol(self):  
        pass
    
    def circle(self, x,y, rad, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, fcol=None):
        if isinstance(lpat, linepat.LinePattern):
            rrad = np.linspace(0, np.pi*2, self._circle_point)
            x1 = x+rad*np.cos(rrad)
            y1 = y+rad*np.sin(rrad)
            self.polygon(x1, y1, lcol, lthk, lpat, fcol)
        else:
            cx = self._x_pixel(x)
            cy = self._y_pixel(y)
            rr = self.get_v(rad)
            self.cntx.arc(cx,cy,rr,0,np.pi*2)
            self.draw_geometry(lcol, lthk*self.frm.hgt(), lpat, fcol)
            
    def symbol(self, x,y, sym):
        px, py = sym.update_xy(self._x_viewport(x),self._y_viewport(y))
        self.polygon(px,py,sym.lcol,sym.lthk,linepat._PAT_SOLID, sym.fcol, viewport=True)
        
    def lline(self, sx, sy, ex, ey, lcol=None, lthk=None, lpat=linepat._PAT_SOLID):
        if lcol: self.make_pen(lcol, lthk*self.frm.hgt())
        #else   : self.make_pen(self.pen.lcol, self.pen.lthk*self.frm.hgt())
        
        if isinstance(lpat, linepat.LinePattern):
            x = [sx, ex]
            y = [sy, ey]
            pat_seg = patline.get_pattern_line(self, x, y, lpat.pat_len, lpat.pat_t, viewport=True)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1[1:], y1[1:]):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
        else:
            self.cntx.move_to(self.get_xl(sx),self.get_yl(sy))
            self.cntx.line_to(self.get_xl(ex),self.get_yl(ey))
            
        self.cntx.stroke()
        
        if lcol: self.delete_pen()
        
    def lmoveto(self, x, y):
        self.cntx.move_to(self.get_xl(x),self.get_yl(y))
        
    def llineto(self, x,y):
        self.cntx.line_to(self.get_xl(x),self.get_yl(y))
    
    def lpolygon(self, x, y, lcol=color.BLACK, lthk=0.001, fcol=None, lpat=linepat._PAT_SOLID):
        self.polygon(x,y,lcol,lthk, lpat, fcol, viewport=True)

    def lpolyline(self, x, y, lcol=color.BLACK, lthk=0.001, lpat=linepat._PAT_SOLID, closed=False):
    
        if isinstance(lpat, linepat.LinePattern):
            if closed:
                if isinstance(x, np.ndarray):
                    xp = np.append(x, x[0])
                    yp = np.append(x, y[0])
                elif isinstance(x, list):
                    xp = x.copy()
                    yp = y.copy()
                    xp.append(x[0])
                    yp.append(y[0])
            else:
                xp = x
                yp = y    
                pat_seg = patline.get_pattern_line(self, xp, yp, lpat.pat_len, lpat.pat_t, viewport=True)
            for p1 in pat_seg:
                x1 = [ p2[0] for p2 in p1 ]
                y1 = [ p2[1] for p2 in p1 ]
                self.cntx.move_to(self.get_xl(x1[0]),self.get_yl(y1[0]))
                for x2, y2 in zip(x1[1:], y1[1:]):
                    self.cntx.line_to(self.get_xl(x2),self.get_yl(y2))
        else:        
            self.create_pnt_list(x,y,self.get_xl,self.get_yl)
            if closed: 
                self.cntx.close_path()
            
        if lcol: self.make_pen(lcol, lthk*self.frm.hgt())    
        else   : self.make_pen(self.pen.lcol, self.pen.lthk*self.frm.hgt())
        self.cntx.stroke()
        if lcol: self.delete_pen()
    
    def create_clip(self, x1, y1, x2, y2):
        self.cntx.save()
        sx=self.get_xl(x1)
        sy=self.get_yl(y1)
        ex=self.get_xl(x2)
        ey=self.get_yl(y2)
        self.cntx.rectangle(sx,sy,ex-sx,ey-sy)
        self.cntx.clip()
        
    def delete_clip(self):
        self.cntx.restore()
        
    def clip(self):    
        return
        
    def save_image(self, fname):
        png = fname.lower().find('.png')
        jpg = fname.lower().find('.jpg')
        if png:
            self.surf.write_to_png(fname)
        elif jpg:
            self.surf.write_to_jpg(fname)
            
    def close(self, format='png'):
        ext = format.lower()
        if ext == 'png':
            self.surf.write_to_png(self.fname)
        elif ext == 'jpg':
            self.surf.write_to_jpg(self.fname)
        self.pnt  = None
        self.cntx = None
        self.surf = None
        self.data = None

class DeviceCairo(DeviceIMG):
    def __init__(self, fname, gbox, dpi=300):
        super().__init__(fname, gbox, dpi)
        
class DeviceCairoAnimation():
    def __init__(self, fname, dev_cairo, func, duration, fps=30, codec='h264'):
        self.fname    = fname
        self.dev      = dev_cairo
        self.func     = func
        self.time     = duration
        self.fps      = fps
        self.codec    = codec
        
    def get_image(self):
        image = np.frombuffer(self.dev.surf.get_data(), np.uint8)
        image = image.reshape((self.dev.surf.get_height(), self.dev.surf.get_width(), 4))
        image = image[:,:,[2,1,0,3]]
        return image[:,:,:3]
        
    def create_frame(self, t):
        self.func(t)
        return self.get_image()
            
    def save_video(self, fname=0):
        fn = fname if fname!=0 else self.fname
        clip = mpy.VideoClip(self.create_frame, duration=self.time)
        clip.write_videofile(fn,self.fps, self.codec)

    def save_gif(self, fname=0):
        fn = fname if fname!=0 else self.fname
        clip = mpy.VideoClip(self.create_frame, duration=self.time)
        clip.write_gif(fn,self.fps)

        